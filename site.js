(function(){'use strict';
function norm(s){return(s||'').toLowerCase().replace(/[\u064B-\u0652\u0640]/g,'').replace(/[أإآ]/g,'ا').replace(/ة/g,'ه').replace(/ى/g,'ي');}
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e;}
document.querySelectorAll('[data-print]').forEach(function(b){b.addEventListener('click',function(){window.print();});});
var box=document.getElementById('results');if(!box)return;
var q=(new URLSearchParams(location.search).get('q')||'').trim();
document.getElementById('q').value=q;
document.getElementById('qtitle').textContent=q?'نتائج البحث: '+q:'ابحث في المنصة';
if(!q)return;
fetch('/search.json').then(function(r){return r.json()}).then(function(d){
  var w=norm(q).split(/\s+/).filter(Boolean);
  var m=d.filter(function(i){var t=norm(i.t+' '+i.x);return w.every(function(k){return t.indexOf(k)>-1});});
  if(!m.length){box.appendChild(el('p','empty','لا توجد نتائج. جرّب كلمات أخرى.'));return;}
  m.forEach(function(i){var d=el('div','li'),h=el('h3'),a=el('a',null,i.t);a.href=i.u;h.appendChild(a);d.appendChild(h);d.appendChild(el('p',null,i.x.slice(0,160)));d.appendChild(el('span','tag',i.s));box.appendChild(d);});
}).catch(function(){box.textContent='تعذّر تحميل البحث.';});
})();
