const lightTrack=$('lightModelTrack'),lightControls=$('lightSliderControls');
const lightPrev=$('lightSliderPrev'),lightNext=$('lightSliderNext'),lightPosition=$('lightSliderPosition');
const visibleLightCards=()=>[...lightTrack.querySelectorAll('[data-light-kind]:not([hidden])')];
let lightSliderFrame=0;
function updateLightSlider(){
 const cards=visibleLightCards(),bounds=lightTrack.getBoundingClientRect();
 const canScroll=lightTrack.scrollWidth>lightTrack.clientWidth+2;
 lightControls.hidden=!canScroll;
 lightPrev.disabled=lightTrack.scrollLeft<=2;
 lightNext.disabled=lightTrack.scrollLeft>=lightTrack.scrollWidth-lightTrack.clientWidth-2;
 const shown=cards.map((card,index)=>{const r=card.getBoundingClientRect();return Math.min(r.right,bounds.right)-Math.max(r.left,bounds.left)>r.width*.5?index+1:0;}).filter(Boolean);
 const start=shown[0]||1,end=shown[shown.length-1]||start;
 lightPosition.textContent=(start===end?start:start+'–'+end)+' из '+cards.length;
}
function moveLightSlider(direction){
 const card=visibleLightCards()[0];if(!card)return;
 const gap=parseFloat(getComputedStyle(lightTrack).columnGap)||0;
 lightTrack.scrollBy({left:direction*(card.getBoundingClientRect().width+gap),behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
}
lightPrev.addEventListener('click',()=>moveLightSlider(-1));
lightNext.addEventListener('click',()=>moveLightSlider(1));
lightTrack.addEventListener('scroll',()=>{if(lightSliderFrame)return;lightSliderFrame=requestAnimationFrame(()=>{lightSliderFrame=0;updateLightSlider();});},{passive:true});
lightTrack.addEventListener('keydown',event=>{if(event.target!==lightTrack)return;if(event.key==='ArrowLeft'||event.key==='ArrowRight'){event.preventDefault();moveLightSlider(event.key==='ArrowLeft'?-1:1);}});
new ResizeObserver(updateLightSlider).observe(lightTrack);
document.querySelectorAll('[data-light-type]').forEach(button=>button.addEventListener('click',()=>{
 const kind=button.dataset.lightType;let count=0;
 document.querySelectorAll('[data-light-type]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
 lightTrack.querySelectorAll('[data-light-kind]').forEach(card=>{card.hidden=kind!=='all'&&card.dataset.lightKind!==kind;if(!card.hidden)count++;});
 $('lightFilterStatus').textContent=({all:'Все модели',diffuse:'Рассеянный свет',directed:'Направленный свет',rotating:'Поворотный свет',adjustable:'Регулируемый свет'}[kind])+' · '+count;
 lightTrack.scrollTo({left:0,behavior:'instant'});updateLightSlider();
}));
requestAnimationFrame(updateLightSlider);
