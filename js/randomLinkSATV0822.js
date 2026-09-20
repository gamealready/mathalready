//specify random links below. You can have as many as you want
var randomlinks=new Array()

randomlinks[0]="SAT_OOS_1.html"
randomlinks[1]="SAT_OOS_2.html"
randomlinks[2]="SAT_OOS_3.html"
randomlinks[3]="SAT_OOS_4.html"
randomlinks[4]="SAT_OOS_5.html"
randomlinks[5]="SAT_OOS_6.html"
randomlinks[6]="SAT_OOS_7.html"
randomlinks[7]="SAT_OOS_8.html"
randomlinks[8]="SAT_OOS_9.html"
randomlinks[9]="SAT_p1_1.html"
randomlinks[10]="SAT_p1_2.html"
randomlinks[11]="SAT_p1_3.html"
randomlinks[12]="SAT_p1_4.html"
randomlinks[13]="SAT_p1_5.html"
randomlinks[14]="SAT_p1_6.html"
randomlinks[15]="SAT_p1_7.html"
randomlinks[16]="SAT_p1_8.html"
randomlinks[17]="SAT_p1_9.html"
randomlinks[18]="SAT_p1_10.html"
randomlinks[19]="SAT_p1_11.html"
randomlinks[20]="SAT_p1_12.html"
randomlinks[21]="SAT_p1_13.html"
randomlinks[22]="SAT_p1_14.html"
randomlinks[23]="SAT_p1_15.html"
randomlinks[24]="SAT_p1_16.html"
randomlinks[25]="SAT_p1_17.html"
randomlinks[26]="SAT_p1_18.html"
randomlinks[27]="SAT_p1_19.html"
randomlinks[28]="SAT_p1_20.html"
//date map to index
var dateToIndex=new Array()





dateToIndex[1]=107;
dateToIndex[2]=108;
dateToIndex[3]=109;
dateToIndex[4]=110;
dateToIndex[5]=111;
dateToIndex[6]=112;
dateToIndex[7]=113;
dateToIndex[8]=6;
dateToIndex[9]=7;
dateToIndex[10]=8;
dateToIndex[11]=9;
dateToIndex[12]=10;
dateToIndex[13]=11;
dateToIndex[14]=12;
dateToIndex[15]=13;
dateToIndex[16]=14;
dateToIndex[17]=15;
dateToIndex[18]=16;
dateToIndex[19]=17;
dateToIndex[20]=18;//5/20
dateToIndex[21]=19;
dateToIndex[22]=20;
dateToIndex[23]=21;
dateToIndex[24]=22;
dateToIndex[25]=23;
dateToIndex[26]=24;
dateToIndex[27]=25;
dateToIndex[28]=26;
dateToIndex[29]=27;
dateToIndex[30]=28;
dateToIndex[31]=29;
function dailyLink(){
    n =  new Date();
    window.location=randomlinks[dateToIndex[n.getDate()]]
}

function randomlink(){
  //not support test mode for now
  let randIndexTemp= Math.floor((Math.random() * 28));
  window.location=randomlinks[randIndexTemp];
  /*
  if (localStorage.getItem("testMode") === null) {
    let randIndex= Math.floor((Math.random() * randomlinks.size()));
    window.location=randomlinks[randIndex];
  }
  if(localStorage.getItem('testMode')==='1'){//test mode
    if(localStorage.getItem('nbrQDone')===localStorage.getItem('nbrQ'))
    {   
        window.location="AMC8_result.html";
    }
    else{
        startNbr=parseFloat(localStorage.getItem('startNbr'));
        nbrQDone=parseFloat(localStorage.getItem('nbrQDone'));
        indexQ=Math.floor((startNbr+nbrQDone)%randomlinks.length);
        localStorage.setItem('indexQ',String(indexQ));
        if(indexQ<randomlinks.length & indexQ>=0){
          window.location=randomlinks[indexQ];
        } else{
          window.location="AMC8_test.html";
        }

        

    }
  }else if(localStorage.getItem('testMode')==='2'){//Challenge mode
    if(localStorage.getItem('nbrQDone')===localStorage.getItem('nbrQDoneCorrectly'))
    {  
      startNbr=parseFloat(localStorage.getItem('startNbr'));
      nbrQDone=parseFloat(localStorage.getItem('nbrQDone'));
      indexQ=Math.floor((startNbr+nbrQDone)%randomlinks.length);
      localStorage.setItem('indexQ',String(indexQ));
      if(indexQ<randomlinks.length & indexQ>=0){
        window.location=randomlinks[indexQ];
      } else{
        window.location="AMC8_challenge.html";
      }
    }else{
      window.location="AMC8_challenge_result.html";
    }
  }else{//random mode ('testMode')==='0'
  let randIndex= Math.floor((Math.random() * randomlinks.length));
    window.location=randomlinks[randIndex];
  }*/
}

 


function Calculate(){
    if(document.isForm.answer.value===localStorage.getItem('rightAnswer')){
      document.isForm.correctOrNot.value="Correct";
    }else{
      document.isForm.correctOrNot.value="Not Correct"
    }
}
  
function NextF()
{
    Calculate();
    //not support test for now
    randomlink();
    /*
    var nbrQDoneN=Number(localStorage.getItem('nbrQDone'));
    if(nbrQDoneN===0){
      var wrongQ = [];
      localStorage.wrongQ = JSON.stringify(wrongQ);
     

    }
    nbrQDoneN+=1;
    localStorage.setItem('nbrQDone',String(nbrQDoneN));
    if(document.isForm.answer.value===localStorage.getItem('rightAnswer')){
      var nbrQDoneCorrectlyN=Number(localStorage.getItem('nbrQDoneCorrectly'));
      nbrQDoneCorrectlyN+=1;  
      localStorage.setItem('nbrQDoneCorrectly',String(nbrQDoneCorrectlyN));
    }else{
      wrongQ = JSON.parse(localStorage.wrongQ);
      indexQ=Number(localStorage.getItem('indexQ'));
      wrongQ.push(indexQ);
      localStorage.wrongQ = JSON.stringify(wrongQ);
    }
    randomlink();*/
}