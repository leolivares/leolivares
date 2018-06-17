#include <HX711.h>
#include <Servo.h>


#define DOUT  A1
#define CLK  A0

HX711 balanza(DOUT, CLK);

Servo miServo;
int angulo=90;
int pinservo = 9;
String readString;
char c;
int endProcess = 0;
int finish;

int finalizar = 0;
float peso;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(2,INPUT);
  pinMode(3,OUTPUT);
  pinMode(4, OUTPUT);
  digitalWrite(3, HIGH);
  
  // Pesar
  Serial.print("Lectura del valor del ADC:  ");
  Serial.println(balanza.read());
  Serial.println("No ponga ningun  objeto sobre la balanza");
  Serial.println("Destarando...");
  Serial.println("...");
  balanza.set_scale(-938978.4689); // Establecemos la escala
  balanza.tare(20);  //El peso actual es considerado Tara.

  //Servo
  miServo.attach(pinservo);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  // Verificar usuario y abrir compuerta


while (Serial.available())
  {
    if (Serial.available() > 0)
    {
      c = Serial.read();  //gets one byte from serial buffer
      readString += c; //makes the string readString
    }
  }

 peso = (balanza.get_units(10));

 if (readString == "getw"){
  
  endProcess = digitalRead(2);

 if (endProcess == 1){
  digitalWrite(4, LOW); //Verde
  digitalWrite(3, HIGH); //Rojo
  readString = "";
  Serial.print("exit"); 
  }

 else if (peso >= 0.05){
    digitalWrite(4, LOW);
    Serial.println("El peso ingresado es mayor a lo posible");
    Serial.println("Retire la botella inmediatamente");
    peso = balanza.get_units(3);
    while(peso >= 0.01){
      digitalWrite(3, LOW);
      delay(250);
      digitalWrite(3, HIGH);
      peso = balanza.get_units(3);
    }   
  }

 else if (peso > 0.01 && peso < 0.05){
    Serial.println(peso);
    Serial.println("Esta es la segunda medida");
    digitalWrite(4, LOW);
    digitalWrite(3, HIGH);
    Serial.println("Ingresando botella");
    delay(500);
    // Pesar
    Serial.print("Peso: ");
    peso = (balanza.get_units(3));
    if (peso < 0.05){
      Serial.print(peso,6);
      Serial.println(" kg");
      balanza.power_down();              // put the ADC in sleep mode
    //  delay(5000);
    //  balanza.power_up();
    
      // Ingresar producto al sistema
      Serial.println("Ingresando peso al sistema...");
      
      // Mover la botella
      balanza.power_up();
      peso = (balanza.get_units(3));
      while(peso > 0.01){
        peso = (balanza.get_units(3));
        angulo = 70;//Maxima velocidad.
        //angulo-=10;//decrementamos 10
        miServo.write(angulo);
      }  
    
      peso = (balanza.get_units(3));
      if (peso <= 0.01){
        angulo = 90;//Maxima velocidad.
        miServo.write(angulo);
      }
    }
    
    else{
      //NADA
    }
  
    // Cerrar sesión
  }
  
  //No se ha detectado codigo QR
  else{
    digitalWrite(4, HIGH);
    digitalWrite(3, LOW);
    Serial.println("Ingrese La Botella...");}
    delay(1000);
  }
}


