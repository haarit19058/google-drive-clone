const express = require('express');
const session = require('express-session');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const archiver = require('archiver');

const app = express();

app.set('view engine', 'ejs');
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));
app.use(session({
  secret: 'your-secret-key',
  resave: false,
  saveUninitialized: true
}));

function isAuthenticated(req, res, next) {
  if (!req.session.username) {
    return res.redirect('/login');
  }
  next();
}

// Multer configuration for handling folder uploads with memory storage
const storage = multer.memoryStorage(); // Store files in memory buffer
const upload = multer({ storage });

// Upload route to handle folder uploads
app.post('/upload', isAuthenticated, upload.any(), (req, res) => {
  const folderName = req.body.folderName;
  const userDir = path.join('uploads', req.session.username, folderName);

  // Create the directory if it doesn't exist
  if (!fs.existsSync(userDir)) {
    fs.mkdirSync(userDir, { recursive: true });
  }

  // Save each file separately in the new directory
  req.files.forEach((file) => {
    const filePath = path.join(userDir, file.originalname);

    // Write the file buffer to the directory
    fs.writeFileSync(filePath, file.buffer);
  });

  res.redirect(`/`);
});



// Routes
app.get('/login', (req, res) => {
  res.send(`
    <form method="POST" action="/login">
      <input type="text" name="username" required>
      <button type="submit">Login</button>
    </form>
  `);
});

app.post('/login', (req, res) => {
  const username = req.body.username;
  if (username) {
    req.session.username = username;
    res.redirect('/');
  } else {
    res.status(400).send('Username is required');
  }
});

app.get('/', isAuthenticated, (req, res) => {
  const userDir = path.join('uploads', req.session.username, req.query.path || '');
  const items = fs.existsSync(userDir)
    ? fs.readdirSync(userDir).map(name => {
        const fullPath = path.join(userDir, name);
        return {
          name,
          isFolder: fs.lstatSync(fullPath).isDirectory()
        };
      })
    : [];

  res.render('index', {
    username: req.session.username,
    items,
    currentPath: req.query.path || ''
  });
});

app.get('/download/:filename', isAuthenticated, (req, res) => {
  const filePath = path.join('uploads', req.session.username, req.query.path || '', req.params.filename);
  if (fs.existsSync(filePath)) {
    res.download(filePath);
  } else {
    res.status(404).send('File not found');
  }
});

app.get('/download-folder/:foldername', isAuthenticated, (req, res) => {
  const folderPath = path.join('uploads', req.session.username, req.query.path || '', req.params.foldername);
  if (!fs.existsSync(folderPath) || !fs.lstatSync(folderPath).isDirectory()) {
    return res.status(404).send('Folder not found');
  }

  const archive = archiver('zip', { zlib: { level: 9 } });
  res.attachment(`${req.params.foldername}.zip`);
  archive.on('error', err => res.status(500).send({ error: err.message }));
  archive.pipe(res);
  archive.directory(folderPath, false);
  archive.finalize();
});

app.post('/logout', (req, res) => {
  req.session.destroy(() => res.redirect('/login'));
});

app.listen(3000, () => console.log('Server running on http://localhost:3000'));
