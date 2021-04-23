#include <Separador.h>      //Libreria para separar string
Separador s;              

#define CIR 5
#define REC 4
#define TRI 0

#define FIG1 14
#define FIG2 12
#define FIG3 13

String el1 = "D";
int sum,sum1,sum2, sum3 = 0;

void setup() {
  Serial.begin(115200);
  pinMode(REC, OUTPUT); 
  pinMode(CIR, OUTPUT); 
  pinMode(TRI, OUTPUT); 

  pinMode(FIG1, OUTPUT); 
  pinMode(FIG2, OUTPUT); 
  pinMode(FIG3, OUTPUT); 
}

void loop() {
  if (Serial.available()){
    serialEvent();  }
}

void serialEvent(){
  String datosrecibidos = Serial.readStringUntil('\n');;
  String el1 = s.separa(datosrecibidos, ',',0);
  String el2 = s.separa(datosrecibidos, ',',1);
  String el3 = s.separa(datosrecibidos, ',',2);
  String el4 = s.separa(datosrecibidos, ',',3);

  //SI ES UN CIRCULO 
  if (el1 == "A"){
    if ((String(el2).toInt() >=40)&&(String(el2).toInt()<=590)&&(String(el3).toInt()>= 90)&&(String(el3).toInt()<=380)){
       sum1 = 1;
    }else{
       sum1 = 0;
    }
 }

  //SI ES UN RECTANGULO
  if (el1 == "R"){
    if ((String(el2).toInt() >=40)&&(String(el2).toInt()<=590)&&(String(el3).toInt()>= 90)&&(String(el3).toInt()<=380)){
      sum2 = 1;
    }else{
      sum2 = 0;
    }
   }
  //SI ES UN TRIANGULO
  if (el1 == "B"){
    if ((String(el2).toInt() >=40)&&(String(el2).toInt()<=590)&&(String(el3).toInt()>= 90)&&(String(el3).toInt()<=380)){
      sum3 = 1;
    }else{
      sum3 = 0;
    }
   }

   
   sum = sum1 + sum2 + sum3;



  //SI SOLO HAY UNA FIGURA
   if (sum ==1){
      
        if(sum1 == 1){
          analogWrite(CIR, 0.88*(String(el2).toInt())-79.2);
          analogWrite(REC, 0);
          analogWrite(TRI, 0);
        }else if (sum1 == 0){
          analogWrite(CIR,0);
        }
        
        if(sum2 == 1){
        analogWrite(REC, 0.46*(String(el3).toInt())-18.4);
        analogWrite(CIR, 0);
        analogWrite(TRI, 0);
        }else if (sum1 == 0){
          analogWrite(REC,0);
        } 
    
        if(sum3 == 1){
        analogWrite(TRI,(String(el4).toInt()));
        analogWrite(REC, 0);
        analogWrite(CIR, 0);
        }else if (sum3 == 0){
          analogWrite(TRI,0);
        } 
  
      
      digitalWrite(FIG1,HIGH);
      digitalWrite(FIG2,LOW);
      digitalWrite(FIG3,LOW);
      
    //SI HAY DOS FIGURAS
   }else if (sum ==2){
        if ((sum1 ==1)&(sum2==1)){
        analogWrite(CIR, 255);
        analogWrite(REC, 255);
        analogWrite(TRI, 0);
        }else if ((sum2 ==1)&(sum3==1)){
        analogWrite(CIR, 0);
        analogWrite(REC, 255);
        analogWrite(TRI, 255);                
        }else if ((sum1 ==1)&(sum3==1)){
        analogWrite(CIR, 255);
        analogWrite(REC, 0);
        analogWrite(TRI, 255);        
        }
      digitalWrite(FIG1,HIGH);
      digitalWrite(FIG2,HIGH);
      digitalWrite(FIG3,LOW);   

      //SI HAY TRES FIGURAS
   }else if (sum ==3){
      digitalWrite(FIG1,HIGH);
      digitalWrite(FIG2,HIGH);
      digitalWrite(FIG3,HIGH); 
      analogWrite(CIR, 255);
      analogWrite(REC, 255);
      analogWrite(TRI, 255);      
   }else{
      digitalWrite(FIG1,LOW);
      digitalWrite(FIG2,LOW);
      digitalWrite(FIG3,LOW);
      analogWrite(CIR, 0);
      analogWrite(TRI, 0);
      analogWrite(REC, 0);
   }

}
