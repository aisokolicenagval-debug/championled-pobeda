const requestDialog=$('documentRequestDialog'),requestForm=$('documentRequestForm'),requestResult=$('documentRequestResult');
let requestTrigger=null,requestReturnScroll=0,lastRequestedSystem='';
function showDocumentRequestForm(){requestForm.hidden=false;requestResult.hidden=true;}
document.querySelectorAll('[data-request-documents]').forEach(trigger=>trigger.addEventListener('click',()=>{
  requestTrigger=trigger;requestReturnScroll=window.scrollY;
  const system='Победа '+(state.edition==='pro'?'Про':'Эко');
  $('requestSystem').value=system;
  $('documentRequestIntro').textContent='Документы для системы «'+system+'». Оставьте контакты и укажите нужные материалы.';
  if(!$('requestMessage').value||$('requestMessage').value===lastRequestedSystem){$('requestMessage').value='Нужны документы для системы «'+system+'».';lastRequestedSystem=$('requestMessage').value;}
  showDocumentRequestForm();requestDialog.showModal();document.body.classList.add('request-dialog-open');
}));
$('closeDocumentRequest').addEventListener('click',()=>requestDialog.close());
requestDialog.addEventListener('click',event=>{if(event.target===requestDialog)requestDialog.close();});
requestDialog.addEventListener('close',()=>{document.body.classList.remove('request-dialog-open');requestTrigger?.focus({preventScroll:true});window.scrollTo({top:requestReturnScroll,behavior:'instant'});});
requestForm.addEventListener('submit',event=>{event.preventDefault();if(!requestForm.reportValidity())return;requestForm.hidden=true;requestResult.hidden=false;requestResult.querySelector('h3').focus({preventScroll:true});});
$('returnDocumentRequest').addEventListener('click',()=>{showDocumentRequestForm();$('requestName').focus({preventScroll:true});});
