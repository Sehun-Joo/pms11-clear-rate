'use strict';
const {rows,buckets,summary}=window.TABLE_DATA;
const $=id=>document.getElementById(id);
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const norm=v=>String(v).normalize('NFKC').toLowerCase().replace(/[^\p{L}\p{N}]/gu,'');
const link=(u,label)=>{try{const x=new URL(u);return /^https?:$/.test(x.protocol)?`<a href="${esc(x.href)}" target="_blank" rel="noopener">${esc(label)} ↗</a>`:'';}catch{return '';}};
$('total').textContent=summary.charts;$('rated').textContent=summary.rated;
for(const b of buckets){const o=document.createElement('option');o.value=b;o.textContent=`${b} (${summary.folders[b]})`;$('folder').append(o);}
function render(){
 const q=norm($('search').value),f=$('folder').value,min=Number($('sample').value);
 const filtered=rows.filter(r=>(!f||r.level===f)&&(!q||norm([r.title,r.artist,r.name_diff,r.ir_title].join(' ')).includes(q))&&(!min||(r.total_plays??0)>=min));
 $('results').textContent=`${filtered.length} charts · highest clear rate first`;$('empty').hidden=filtered.length>0;
 $('rows').innerHTML=filtered.map(r=>`<tr><td><span class="badge">${r.clear_rate===null?'No data':esc(r.clear_rate.toFixed(1))+'%'}</span><span class="chart-meta">${esc(r.level)}</span></td><td><div class="song-name">${esc(r.title)}</div><span class="artist">${esc(r.artist)}</span><span class="chart-name">${esc(r.name_diff||'')}</span><span class="comment">${esc(r.comment)}</span></td><td><div>${r.total_plays===null?'Unknown':esc(r.total_clears??'?')+' / '+esc(r.total_plays)+' plays'}</div>${r.total_plays>0&&r.total_plays<10?'<span class="tag">Small sample</span>':''}<span class="chart-meta">${r.rate_method==='displayed_play_clear_rate'?'Mocha per-play rate':r.clear_rate!==null?'Calculated per-play rate':'No usable rate'}</span></td><td><div class="links">${link(r.mocha_url,'Mocha IR')}${link(r.url,'Song / package')}${link(r.url_diff,'Chart')}</div></td></tr>`).join('');
}
$('search').addEventListener('input',render);for(const id of ['folder','sample'])$(id).addEventListener('change',render);render();
