"""Build a fixed, auditable Mocha player-clear-rate snapshot for PMS Database 11."""
import argparse, json, html
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BUCKETS=['90-100%','80-<90%','70-<80%','60-<70%','50-<60%','40-<50%','30-<40%','20-<30%','10-<20%','0-<10%','No data']
def main():
 p=argparse.ArgumentParser();p.add_argument('--base-url',default='');args=p.parse_args()
 source=json.loads((ROOT/'source-level11.json').read_text(encoding='utf-8'))
 stats=json.loads((ROOT/'mocha-stats.json').read_text(encoding='utf-8'))
 by_hash={s['md5']:s for s in stats};assert len(by_hash)==len(source)
 rows=[];counts={b:0 for b in BUCKETS}
 for original in source:
  assert str(original['level'])=='11'
  s=by_hash[original['md5']];rate=s.get('rate');total=s.get('total_users')
  if rate is None:bucket='No data'
  else:
   assert 0<=rate<=100 and total>0
   bucket=BUCKETS[9-min(9,int(rate//10))]
  counts[bucket]+=1
  text=f"Mocha player clear rate: {rate:g}% ({s['clear_users']}/{total} users)" if rate is not None else 'Mocha player clear rate: unavailable'
  if rate is not None and total<10:text+='; small sample (<10 users)'
  rows.append(dict(original,level=bucket,original_level='11',comment=text+' · Snapshot 2026-10-23 · '+original.get('comment',''),clear_rate=rate,total_users=total,clear_users=s.get('clear_users'),rate_method=s.get('method'),mocha_url=s['url'],statistics_status=s['status'],ir_title=s.get('ir_title','')))
 assert len({r['md5'] for r in rows})==len(source)
 rows.sort(key=lambda r:(BUCKETS.index(r['level']),-(r['clear_rate'] or 0),-(r['total_users'] or 0),r['title'].casefold()))
 base=args.base_url.rstrip('/');url=lambda f:base+'/'+f if base else f
 dist=ROOT/'dist';dist.mkdir(exist_ok=True)
 header=dict(name='PMS Database ●11 — Mocha clear-rate folders',symbol='●11 CR ',data_url=url('data.json'),level_order=BUCKETS)
 summary=dict(charts=len(rows),rated=sum(r['clear_rate'] is not None for r in rows),no_data=counts['No data'],small_samples=sum(r['clear_rate'] is not None and r['total_users']<10 for r in rows),folders=counts,snapshot='2026-10-23')
 for name,data in [('data.json',rows),('header.json',header),('summary.json',summary)]:
  (dist/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (dist/'data.js').write_text('window.TABLE_DATA='+json.dumps(dict(rows=rows,buckets=BUCKETS,summary=summary),ensure_ascii=False).replace('<','\\u003c')+';\n',encoding='utf-8')
 # Ship the full chart list in HTML so script failures cannot hide the table.
 esc=lambda value:html.escape(str(value if value is not None else ''),quote=True)
 def link(target,label):
  return f'<a href="{esc(target)}" target="_blank" rel="noopener">{esc(label)} ↗</a>' if target and target.startswith(('https://','http://')) else ''
 rendered=[]
 for r in rows:
  rate=f"{r['clear_rate']:.1f}%" if r['clear_rate'] is not None else 'No data'
  players=f"{r['clear_users']} / {r['total_users']} players" if r['total_users'] is not None else 'Unknown'
  small='<span class="tag">Small sample</span>' if r['total_users'] and r['total_users']<10 else ''
  links=link(r['mocha_url'],'Mocha IR')+link(r.get('url'),'Song / package')+link(r.get('url_diff'),'Chart')
  rendered.append(f'<tr><td><span class="badge">{esc(rate)}</span><span class="chart-meta">{esc(r["level"])}</span></td><td><div class="song-name">{esc(r["title"])}</div><span class="artist">{esc(r["artist"])}</span><span class="chart-name">{esc(r.get("name_diff"))}</span><span class="comment">{esc(r["comment"])}</span></td><td>{esc(players)}{small}</td><td><div class="links">{links}</div></td></tr>')
 page=(ROOT/'page.html').read_text(encoding='utf-8').replace('@@HEADER_URL@@',esc(url('header.json')))
 page=page.replace('<tbody id="rows"></tbody>','<tbody id="rows">'+''.join(rendered)+'</tbody>')
 page=page.replace('<strong id="total"></strong>',f'<strong id="total">{len(rows)}</strong>').replace('<b id="rated"></b>',f'<b id="rated">{summary["rated"]}</b>')
 page=page.replace('id="results" role="status" aria-live="polite"></p>',f'id="results" role="status" aria-live="polite">{len(rows)} charts · highest clear rate first</p>')
 page=page.replace('<div class="toolbar">','<noscript><p>The full chart list is below. Enable JavaScript to use search and filters.</p></noscript><div class="toolbar">')
 (dist/'index.html').write_text(page,encoding='utf-8')
 print(json.dumps(summary))
if __name__=='__main__':main()
