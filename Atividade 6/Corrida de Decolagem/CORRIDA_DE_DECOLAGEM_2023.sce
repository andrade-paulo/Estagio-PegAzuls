/* 
Autor: Clinton Noberto Silva Araújo
e-mail: clinton_noberto@hotmail.com
Subsistema: Desempenho
Equipe: PegAzuls Aerodesign
*/

close
clear
clc


//==========================CONSTANTES VARIAVEIS======================//

S = 1.5;                               //Área de Asa em [m^2]
Sht = 0.180;
Cl = 1.80395;                         //Coeficiente de Sustentação [-]1
Clht = -0.2776;
Cdht = 0.0117671843;
Cdvt = 0.014909;
Cd0 = 0.031706366;                            //Coeficiênte de Arrasto Parasita [-]
K = 0.0733106672;                              //Fator de Arrasto Induzido [-]
Kht = 0.102822572;
SGAP = 0.06                           // MONOPLANO USAR "ZERO", BIPLANO "0,06"
//==========================ESTIMATIVA PESO VAZIO======================//

//OBS.: LEVANDO EM CONSIDERAÇÃO APENAS ASA,GAP E EMPENAGEM  
Sasabase = 0.984 //´ÁREA DA ASA USADA COMO BASE (m²)
Pasabase = 1633 // PESO DA ASA USADA COMO BASE (g)
Sehbase = 0.16 // ÁREA DA EMPENAGEM HORIZONTAL USADA COMO BASE (m²)
Pehbase = 258 // PESO DA EH USADA COMO BASE (g)
SGAPbase = 0.12 // ÁREA DOS GAP USADA COMO BASE (m²)
PGAPbase = 266 // PESO DOS GAP USADO COMO BASE (g)

Pasaatual =(Pasabase*S)/Sasabase // PESO DA ASA ATUAL (g)
Pehatual =(Pehbase*Sht)/Sehbase// PESO DA EH ATUAL (g)
PGAPatual =(PGAPbase*SGAP)/SGAPbase // PESO DO GAP ATUAL

Somapatual = Pasaatual+Pehatual+PGAPatual // SOMA DOS PESOS DOS PARAMETROS 
Somapbase = Pasabase+Pehbase+PGAPbase

PVbase = 3260 // PESO VAZIO USADO COMO BASE (g)
PVatual = (PVbase*Somapatual)/Somapbase // ETIMATIVA DO PESO VAZIO DE SUA AERONAVE


//==============================CONSTANTES============================//

g = 9.81;                               //Aceleração da Gravidade em [m/s^2]

f = 0.9072;                              //Fator para Tração em [N.s^2/m]
mi = 0.0270;                             //Coeficiente de Atrito Cinético das Rodas[-]
r = 1.1132;                              //Densidade do Ar em [kg/m^3]
xlim=55;                                //Limite de Comprimento da Pista em [m]
h=10^-2;                                //Passo de Integração em [s]

//==========================CONDIÇÕES INICIAIS===========================//
m(1) = 5;                               //Massa do Avião em [kg]
w(1) = m(1)*g;                          //Peso do Avião em [N]
t(1) = 0;                               //Tempo Inicial em [s]
vx(1) = 0;                              //Velocidade x Inicial em [m/s]
vy(1) = 0;                              //Velocidade y Inicial em [m/s]
x(1) = 0;                               //Posição x Inicial em [m]
y(1) = 0;                               //Posição y Inicial em [m]
T(1) = (47.782-(vx(1)^2))*f;                    //Tração em [N]

D(1) = 0.5*r*vx(1)^2*S*(Cd0 + K*Cl^2 + Cdht*(Sht/S)*Kht);    //Arrasto em [N]

L(1) = 0.5*r*vx(1)^2*S*(Cl);            //Sustentação em [N]
Fr(1) = mi*abs(L(1)-w(1));              //Atrito das Rodas em [N]
ax(1) = (T(1)-D(1)-Fr(1))/m(1);         //Aceleração x em [m/s^2]
ay(1) = 0;                              //Aceleração y em [m/s^2]
//=======================================================================//

//==========================INTEGRAÇÃO NUMÉRICA==========================//

for j=1:1:2000

    printf('\nNumero de iteração %d\n', j)
    i=1;
    x(1)=0;
    w(j) = m(j)*g;
    m(j+1) = m(j) + 0.01;

    while x(i) < xlim
        
        t(i+1)=t(i)+h;
        vx(i+1)=vx(i)+ax(i)*h;
        x(i+1)=x(i)+vx(i+1)*h;
        T(i+1) = (47.782-(vx(1)^2))*f;
        D(i+1) = 0.5*r*vx(i+1)^2*S*(Cd0+K*Cl^2);
        
        L(i+1) = 0.5*r*vx(i+1)^2*S*(Cl)*1.14;
        
        if  L(i+1)<w(j)
            Fr(i+1) = mi*abs(L(i+1)-w(j));
            ay(i+1) = 0;
            vy(i+1) = 0;
            y(i+1) = 0;
                      
        else
            Fr(i+1) = 0;
            ay(i+1) = (L(i+1)-w(j))/m(j);
            vy(i+1) = vy(i)+ay(i)*h;
            y(i+1) = y(i)+vy(i+1)*h;
        end
        
    
        ax(i+1) = (T(i+1)-D(i+1)-Fr(i+1))/m(j);
        i=i+1;
    end
    
    printf('Altura: %.2f cm\n',y(i)*100)
    printf('Peso: %.2f kgf\n',w(j)/g)
    
    CP = ( w(j)/g )  //carga paga
    
    if y(i) > 0.70 && y(i) < 0.75
        
        printf('\n\n             ======LIMITE DE PISTA: 55 m ======')
        printf('\n              ================================\n')
        printf('              Sustentação: %.2f kgf\n',L(i)/g)
        printf('              ================================\n')
        printf('              Tempo: %.2f s',t(i))
        printf('\n              ================================\n')
        printf('              Altura: %.2f cm',y(i)*100)
        printf('\n              ================================\n')
        printf('              MTOW: %.2f kg\n',w(j)/g)
        printf('              ================================\n')
        printf("              Peso vazio: %.2f kg\n",PVatual/1000)
        printf('              ================================\n')
        printf("              Carga paga: %.2f kg\n",CP - (PVatual/1000))
        printf('              ================================\n\n\n\n')
        
        
        //plot graficos
        w0=linspace(w(j),w(j),i)'; //Vetor Peso em [N]
        
        subplot(1,2,1)
        plot(t,T,'-*',t,D,'-*',t,L,'-*',t,Fr,'-*',t,w0,'-*')
        legend('$Tração$','$Arrasto$','$Sustentação$','$Atrito$','$Peso$',2)
        title('$Cinética\quad da\quad Aeronave$','fontsize',4.5)
        xlabel('$Tempo\quad(s)$','fontsize',4)
        ylabel('$Forças$','fontsize',4)
        xgrid
        
        subplot(1,2,2)
        plot(t,x,'-*',t,vx,'-*',t,ax,'-*',t,y,'-*',t,vy,'-*',t,ay,'-*')
        legend('$Posição\quad x$','$Velocidade\quad x$','$Aceleração\quad x$','$Posição\quad y$','$Velocidade\quad y$','$Aceleração\quad y$',2)
        title('$Cinemática\quad da\quad  Aeronave$','fontsize',4.5)
        xlabel('$Tempo\quad(s)$','fontsize',4)
        ylabel('$Movimento$','fontsize',4)
        xgrid

        break
     end
end
//=======================================================================//






