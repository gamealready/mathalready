//specify random links below. You can have as many as you want
var randomlinks=new Array()

randomlinks[0]="AMC8_2022_1.html"
randomlinks[1]="AMC8_2022_2.html"
randomlinks[2]="AMC8_2022_3.html"
randomlinks[3]="AMC8_2022_5.html"
randomlinks[4]="AMC8_2022_6.html"
randomlinks[5]="AMC8_2022_7.html"
randomlinks[6]="AMC8_2023_22.html"
randomlinks[7]="AMC8_2023_21.html"
randomlinks[8]="AMC8_2023_20.html"
randomlinks[9]="AMC8_2023_19.html"
randomlinks[10]="AMC8_2023_18.html"
randomlinks[11]="AMC8_2023_17.html"
randomlinks[12]="AMC8_2023_16.html"
randomlinks[13]="AMC8_2023_15.html"
randomlinks[14]="AMC8_2023_14.html"
randomlinks[15]="AMC8_2023_13.html"
randomlinks[16]="AMC8_2023_12.html"
randomlinks[17]="AMC8_2023_11.html"
randomlinks[18]="AMC8_2023_10.html"
randomlinks[19]="AMC8_2023_9.html"
randomlinks[20]="AMC8_2023_8.html"
randomlinks[21]="AMC8_2023_7.html"
randomlinks[22]="AMC8_2023_6.html"
randomlinks[23]="AMC8_2023_5.html"
randomlinks[24]="AMC8_2023_4.html"
randomlinks[25]="AMC8_2023_3.html"
randomlinks[26]="AMC8_2023_2.html"
randomlinks[27]="AMC8_2023_1.html"
randomlinks[28]="AMC8_2023_23.html"
randomlinks[29]="AMC8_2023_24.html"
randomlinks[30]="AMC8_2023_25.html"
randomlinks[31]="AMC8_2022_4.html"

//specify random links below. You can have as many as you want
var dateToIndex=new Array()
dateToIndex[23]=28;
dateToIndex[24]=29;
dateToIndex[25]=30;
dateToIndex[26]=31;
function dailyLink(){
    n =  new Date();
    window.location=randomlinks[dateToIndex[n.getDate()]]
}

function randomlink(){
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
    var nbrQDoneN=Number(localStorage.getItem('nbrQDone'));
    if(nbrQDoneN==0){
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
    randomlink();
}