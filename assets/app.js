const state={links:[],category:'all',query:''};
const $=s=>document.querySelector(s);
const normaliseName=value=>String(value||'').replace(/^.*?\s\/\s/,'').replace(/[-_]/g,' ').replace(/\b\w/g,c=>c.toUpperCase()).trim();

async function load(){
  const response=await fetch('data/links.json');
  if(!response.ok)throw new Error('Could not load library data');
  const data=await response.json();
  state.links=(data.links||[]).map(link=>({...link,name:(link.name||'').trim()||normaliseName(link.githubRepo||link.domain)}));
  renderCategories();render();
}
function categories(){return [...new Set(state.links.map(x=>x.category).filter(Boolean))].sort();}
function renderCategories(){
  const el=$('#categories');el.innerHTML='';
  [['all','ALL RESOURCES'],...categories().map(c=>[c,c.toUpperCase()])].forEach(([value,label])=>{
    const button=document.createElement('button');button.type='button';button.className=`category-btn ${state.category===value?'active':''}`;button.textContent=label;
    button.addEventListener('click',()=>{state.category=value;renderCategories();render();});el.append(button);
  });
}
function visible(){const q=state.query.toLowerCase().trim();return state.links.filter(link=>{
  const categoryMatches=state.category==='all'||link.category===state.category;
  const searchable=[link.name,link.description,link.category,link.githubRepo,link.domain].filter(Boolean).join(' ').toLowerCase();
  return categoryMatches&&(!q||searchable.includes(q));
});}
function makeCard(link){
  const card=$('#card-template').content.firstElementChild.cloneNode(true);
  card.querySelector('.card-category').textContent=link.category.toUpperCase();
  const pick=card.querySelector('.pick');pick.hidden=!link.pick;
  card.querySelector('h3').textContent=link.name;
  card.querySelector('.description').textContent=link.description||'Open this resource to explore it.';
  const open=card.querySelector('.open');open.href=link.url;open.setAttribute('aria-label',`Open ${link.name}`);
  return card;
}
function render(){
  const links=visible(),resources=$('#resources'),empty=$('#empty');resources.innerHTML='';
  $('#count').textContent=`${links.length} RESOURCE${links.length===1?'':'S'}`;
  empty.hidden=links.length>0;
  if(!links.length)return;
  const groups=new Map();links.forEach(link=>{const key=link.category||'Other';if(!groups.has(key))groups.set(key,[]);groups.get(key).push(link);});
  [...groups.entries()].sort(([a],[b])=>a.localeCompare(b)).forEach(([category,items])=>{
    const section=document.createElement('section');section.className='category-section';
    const heading=document.createElement('h2');heading.className='category-heading';heading.textContent=category.toUpperCase();section.append(heading);
    const grid=document.createElement('div');grid.className='category-grid';items.sort((a,b)=>a.name.localeCompare(b.name)).forEach(link=>grid.append(makeCard(link)));section.append(grid);resources.append(section);
  });
}
$('#search').addEventListener('input',event=>{state.query=event.target.value;render();});
$('#clear').addEventListener('click',()=>{$('#search').value='';state.query='';render();});
load().catch(error=>{console.error(error);$('#count').textContent='FAILED TO LOAD';});
