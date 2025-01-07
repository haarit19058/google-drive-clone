char message[]="sos";

int morse_a[]={2,1,0};
int morse_b[]={4,1,0,0,0};
int morse_c[]={4,1,0,1,0};
int morse_d[]={3,1,0,0};
int morse_e[]={2,1,0};
int morse_f[]={4,0,0,1,0};
int morse_g[]={3,1,1,0};
int morse_h[]={4,0,0,0,0};
int morse_i[]={2,0,0};
int morse_j[]={4,0,1,1,1};
int morse_k[]={3,1,0,1};
int morse_l[]={4,0,1,0,0};
int morse_m[]={2,1,1};

int morse_n[]={2,1,0};
int morse_o[]={3,1,1,1};
int morse_p[]={4,0,1,1,0};
int morse_q[]={4,1,1,0,1};
int morse_r[]={3,0,1,0};
int morse_s[]={3,0,0,0};
int morse_t[]={1,1};
int morse_u[]={3,0,0,1};
int morse_v[]={4,0,0,0,1};
int morse_w[]={3,0,1,1};
int morse_x[]={4,1,0,0,1};
int morse_y[]={4,1,0,1,1};
int morse_z[]={4,1,1,0,0};

int morse_1[]={5,0,1,1,1,1};
int morse_2[]={5,0,0,1,1,1};
int morse_3[]={5,0,0,0,1,1};
int morse_4[]={5,0,0,0,0,1};
int morse_5[]={5,0,0,0,0,0};
int morse_6[]={5,1,0,0,0,0};
int morse_7[]={5,1,1,0,0,0};
int morse_8[]={5,1,1,1,0,0};
int morse_9[]={5,1,1,1,1,0};
int morse_10[]={5,1,1,1,1,1};
int morse_11[]={1,-1};


void morse(int *arr,int l,int pin){
  for (int i=0;i<l;i++){
    if (*(arr+i)==1){
      digitalWrite(pin, HIGH);  // turn the LED on (HIGH is the voltage level)
      delay(800);                      // wait for a second
      digitalWrite(pin, LOW);   // turn the LED off by making the voltage LOW
      delay(100);                      // wait for a second
    }
    // else if (arr==-1){
    //   digitalWrite(pin, LOW);   // turn the LED off by making the voltage LOW
    //   delay(1200);
    // }
    else{
      digitalWrite(pin, HIGH);  // turn the LED on (HIGH is the voltage level)
      delay(400);                      // wait for a second
      digitalWrite(pin, LOW);   // turn the LED off by making the voltage LOW
      delay(100); 
    }
  }
}

int* encode(char msg){
    if (msg=='a' || msg=='A') return morse_a;
    else if (msg=='b' || msg=='B') return morse_b;
    else if (msg=='c' || msg=='C') return morse_c;
    else if (msg=='d' || msg=='D') return morse_d;
    else if (msg=='e' || msg=='E') return morse_e;
    else if (msg=='f' || msg=='F') return morse_f;
    else if (msg=='g' || msg=='G') return morse_g;
    else if (msg=='h' || msg=='H') return morse_h;
    else if (msg=='i' || msg=='I') return morse_i;
    else if (msg=='j' || msg=='J') return morse_j;
    else if (msg=='k' || msg=='K') return morse_k;
    else if (msg=='l' || msg=='L') return morse_l;
    else if (msg=='m' || msg=='M') return morse_m;
    else if (msg=='n' || msg=='N') return morse_n;
    else if (msg=='o' || msg=='O') return morse_o;
    else if (msg=='p' || msg=='P') return morse_p;
    else if (msg=='q' || msg=='Q') return morse_q;
    else if (msg=='r' || msg=='R') return morse_r;
    else if (msg=='s' || msg=='S') return morse_s;
    else if (msg=='t' || msg=='T') return morse_t;
    else if (msg=='u' || msg=='U') return morse_u;
    else if (msg=='v' || msg=='V') return morse_v;
    else if (msg=='w' || msg=='W') return morse_w;
    else if (msg=='x' || msg=='X') return morse_x;
    else if (msg=='y' || msg=='Y') return morse_y;
    else if (msg=='z' || msg=='Z') return morse_z;
    else if (msg=='1') return morse_1;
    else if (msg=='2') return morse_2;
    else if (msg=='3') return morse_3;
    else if (msg=='4') return morse_4;
    else if (msg=='5') return morse_5;
    else if (msg=='6') return morse_6;
    else if (msg=='7') return morse_7;
    else if (msg=='8') return morse_8;
    else if (msg=='9') return morse_9;
    else if (msg=='10') return morse_10;
    else if (msg==' ') return morse_11;
}

void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(0, OUTPUT);
}



// the loop function runs over and over again forever
void loop() {
  int len=sizeof(message)/sizeof(message[0]);
  for (int i=0;i<len-1;i++){
    int *arr=encode(message[i]);
    int l_arr=*arr;
    Serial.println(message[i]);
    morse(arr+1,l_arr,0);
  }
  digitalWrite(0,LOW);
  delay(2000);
}