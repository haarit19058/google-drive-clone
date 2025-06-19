const express = require('express');
const session = require('express-session');
const multer = require('multer');
const path = require('path');
const fs = require('fs').promises;
const fsSync = require('fs');
const archiver = require('archiver');
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');
const MongoStore = require('connect-mongo');
require('dotenv').config();

// Import models
const Users = require("./Models/user.js");

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 3000;

// Database connection
async function connectToDatabase() {
  try {
    await mongoose.connect(process.env.MONGODB_URI || "mongodb+srv://haarit:haarit1905@cluster0.388wn.mongodb.net/");
    console.log("✅ Connected to MongoDB");
  } catch (error) {
    console.error("❌ Database connection failed:", error);
    process.exit(1);
  }
}

// Middleware setup
app.set('view engine', 'ejs');
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static('public'));

// Session configuration with MongoDB store
app.use(session({
  secret: process.env.SESSION_SECRET || 'your-secret-key-change-in-production',
  resave: false,
  saveUninitialized: false,
  store: MongoStore.create({
    mongoUrl: process.env.MONGODB_URI || "mongodb+srv://haarit:haarit1905@cluster0.388wn.mongodb.net/",
    touchAfter: 24 * 3600 // lazy session update
  }),
  cookie: {
    secure: process.env.NODE_ENV === 'production',
    httpOnly: true,
    maxAge: 1000 * 60 * 60 * 24 * 7 // 7 days
  }
}));

// Authentication middleware
function isAuthenticated(req, res, next) {
  if (!req.session.username) {
    return res.redirect('/login');
  }
  next();
}

// Create uploads directory if it doesn't exist
async function ensureUploadsDir() {
  const uploadsDir = path.join(__dirname, 'uploads');
  try {
    await fs.access(uploadsDir);
  } catch {
    await fs.mkdir(uploadsDir, { recursive: true });
  }
}

// Multer configuration
const storage = multer.memoryStorage();
const upload = multer({ 
  storage,
  limits: {
    fileSize: 100 * 1024 * 1024, // 100MB limit per file
    files: 1000 // Max 1000 files per upload
  },
  fileFilter: (req, file, cb) => {
    // Add file type restrictions if needed
    cb(null, true);
  }
});

// Utility function to create user directory
async function ensureUserDirectory(username, additionalPath = '') {
  const userDir = path.join(__dirname, 'uploads', username, additionalPath);
  try {
    await fs.access(userDir);
  } catch {
    await fs.mkdir(userDir, { recursive: true });
  }
  return userDir;
}

// Routes

// Login/Register page
app.get('/login', (req, res) => {
  const error = req.query.error;
  res.send(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>Login - Drive Clone</title>
      <style>
        body { font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; }
        .form-container { background: #f9f9f9; padding: 30px; border-radius: 8px; margin-bottom: 20px; }
        .form-container h2 { margin-top: 0; color: #333; }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #4285f4; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #3367d6; }
        .error { color: red; margin: 10px 0; }
      </style>
    </head>
    <body>
      ${error ? `<div class="error">Error: ${error}</div>` : ''}
      
      <div class="form-container">
        <h2>Login</h2>
        <form method="POST" action="/login">
          <input type="email" name="username" placeholder="Email" required>
          <input type="password" name="password" placeholder="Password" required>
          <button type="submit">Login</button>
        </form>
      </div>

      <div class="form-container">
        <h2>Register</h2>
        <form method="POST" action="/register">
          <input type="email" name="username" placeholder="Email" required>
          <input type="password" name="password" placeholder="Password (min 6 chars)" minlength="6" required>
          <button type="submit">Register</button>
        </form>
      </div>
    </body>
    </html>
  `);
});

// Register route
app.post("/register", async (req, res) => {
  try {
    const { username, password } = req.body;
    
    // Validate input
    if (!username || !password) {
      return res.redirect('/login?error=Email and password are required');
    }
    
    if (password.length < 6) {
      return res.redirect('/login?error=Password must be at least 6 characters');
    }

    // Check if user already exists
    const existingUser = await Users.findOne({ email: username });
    if (existingUser) {
      return res.redirect('/login?error=User already exists');
    }

    // Hash password
    const saltRounds = 12;
    const hashedPassword = await bcrypt.hash(password, saltRounds);

    // Create user
    await Users.create({ 
      email: username, 
      password: hashedPassword 
    });

    // Create user directory
    await ensureUserDirectory(username);

    res.redirect('/login?success=Registration successful, please login');
  } catch (error) {
    console.error('Registration error:', error);
    res.redirect('/login?error=Registration failed');
  }
});

// Login route
app.post('/login', async (req, res) => {
  try {
    const { username, password } = req.body;

    if (!username || !password) {
      return res.redirect('/login?error=Email and password are required');
    }

    const user = await Users.findOne({ email: username });
    if (!user) {
      return res.redirect('/login?error=Invalid credentials');
    }

    const isValidPassword = await bcrypt.compare(password, user.password);
    if (!isValidPassword) {
      return res.redirect('/login?error=Invalid credentials');
    }

    req.session.username = username;
    res.redirect('/');
  } catch (error) {
    console.error('Login error:', error);
    res.redirect('/login?error=Login failed');
  }
});

// Main dashboard
app.get('/', isAuthenticated, async (req, res) => {
  try {
    const currentPath = req.query.path || '';
    const userDir = path.join(__dirname, 'uploads', req.session.username, currentPath);
    
    let items = [];
    try {
      await fs.access(userDir);
      const files = await fs.readdir(userDir);
      
      items = await Promise.all(
        files.map(async (name) => {
          const fullPath = path.join(userDir, name);
          const stats = await fs.lstat(fullPath);
          return {
            name,
            isFolder: stats.isDirectory(),
            size: stats.isFile() ? stats.size : null,
            modified: stats.mtime
          };
        })
      );
    } catch (error) {
      // Directory doesn't exist or can't be read
      console.log('Directory access error:', error.message);
    }

    res.render('index', {
      username: req.session.username,
      items,
      currentPath
    });
  } catch (error) {
    console.error('Dashboard error:', error);
    res.status(500).send('Internal server error');
  }
});

// Upload route
app.post('/upload', isAuthenticated, upload.any(), async (req, res) => {
  try {
    const folderName = req.body.folderName;
    if (!folderName) {
      return res.status(400).send('Folder name is required');
    }

    const userDir = await ensureUserDirectory(req.session.username, folderName);

    // Process uploaded files
    for (const file of req.files) {
      const fileName = file.originalname;
      const filePath = path.join(userDir, fileName);
      
      // Ensure subdirectories exist
      const fileDir = path.dirname(filePath);
      await fs.mkdir(fileDir, { recursive: true });
      
      // Write file
      await fs.writeFile(filePath, file.buffer);
    }

    res.redirect('/');
  } catch (error) {
    console.error('Upload error:', error);
    res.status(500).send('Upload failed');
  }
});

// Download file
app.get('/download/:filename', isAuthenticated, async (req, res) => {
  try {
    const filePath = path.join(__dirname, 'uploads', req.session.username, req.query.path || '', req.params.filename);
    
    await fs.access(filePath);
    res.download(filePath);
  } catch (error) {
    console.error('Download error:', error);
    res.status(404).send('File not found');
  }
});

// Download folder as zip
app.get('/download-folder/:foldername', isAuthenticated, async (req, res) => {
  try {
    const folderPath = path.join(__dirname, 'uploads', req.session.username, req.query.path || '', req.params.foldername);
    
    const stats = await fs.lstat(folderPath);
    if (!stats.isDirectory()) {
      return res.status(404).send('Folder not found');
    }

    const archive = archiver('zip', { zlib: { level: 9 } });
    
    res.attachment(`${req.params.foldername}.zip`);
    archive.on('error', (err) => {
      console.error('Archive error:', err);
      res.status(500).send('Archive creation failed');
    });
    
    archive.pipe(res);
    archive.directory(folderPath, false);
    await archive.finalize();
  } catch (error) {
    console.error('Folder download error:', error);
    res.status(404).send('Folder not found');
  }
});

// Logout route
app.post('/logout', (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      console.error('Logout error:', err);
    }
    res.redirect('/login');
  });
});

// Error handling middleware
app.use((error, req, res, next) => {
  console.error('Unhandled error:', error);
  res.status(500).send('Internal server error');
});

// 404 handler
app.use((req, res) => {
  res.status(404).send('Page not found');
});

// Start server
async function startServer() {
  await connectToDatabase();
  await ensureUploadsDir();
  
  app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
  });
}

startServer().catch(console.error);
