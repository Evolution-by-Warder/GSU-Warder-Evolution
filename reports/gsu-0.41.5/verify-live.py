"""Check the public GSU release against its installed and deployed records."""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import time
from urllib.request import Request, urlopen

HERE=Path(__file__).resolve().parent
GH='https://api.github.com/repos/Evolution-by-Warder/'
RAW='https://raw.githubusercontent.com/Evolution-by-Warder/'
GSU='GSU-Warder-Evolution'
WEB='YouTube-Warder-Evolution'
SITE='https://warder-evolution.eu/'
VERSION='0.41.5'
TAG='v'+VERSION


def fetch(url,limit):
    request=Request(url,headers={'Cache-Control':'no-cache','User-Agent':'Warder-GSU-release-audit'})
    with urlopen(request,timeout=30) as response:
        content=response.read(limit+1)
    if len(content)>limit:
        raise ValueError('unexpected response size for '+url)
    return content


def get_json(url):return json.loads(fetch(url,1048576))


class Portal(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=set()
        self.languages=set()
        self.text=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='a' and a.get('href'):self.links.add(a['href'])
        if tag=='span' and 'lang' in a:self.languages.add(a['lang'])
    def handle_data(self,data):self.text.append(data)


def main():
    closeout=json.loads((HERE/'closeout.json').read_text())
    public=json.loads((HERE/'public-verification.json').read_text())
    report=get_json(RAW+GSU+'/main/plugin/update/stable-modern.json')
    release=report['release']
    local=json.loads((HERE.parents[1]/'PRODUCTION.json').read_text())
    assert local['release']==release
    assert local['update_feeds'][0]==RAW+GSU+'/main/plugin/update/stable-modern.json'
    assert set(local['feed_roles']['r6_compatibility'])=={RAW+GSU+'/'+branch+'/plugin/update/stable.json' for branch in ('main','original-python314')}
    assert report['channel']=='stable-modern' and release['tag']==TAG and release['version']==VERSION
    assert release['sha256']==public['public_sha256'] and release['bytes']==public['public_bytes']
    assert get_json(GH+GSU+'/git/ref/tags/'+TAG)['object']['sha']==public['source_commit']
    published=get_json(GH+GSU+'/releases/tags/'+TAG)
    assert not published['draft'] and not published['prerelease']
    raw=fetch(release['url'],release['bytes'])
    assert len(raw)==release['bytes'] and hashlib.sha256(raw).hexdigest()==release['sha256']
    assert fetch(release['url']+'.sha256',1024).decode().split()==[release['sha256'],release['url'].rsplit('/',1)[1]]
    for branch in ('main','original-python314'):
        base=RAW+GSU+'/'+branch+'/'
        old=get_json(base+'plugin/update/stable.json')['release']
        assert (old['version'],old['sha256'])==('13.41-r6','a8e79609147666b27f18460b3340e099bb013664478a787746bcf56bb28052e2')
        for bridge in ('plugin/update/candidate.json','restoration/update/candidate.json'):
            assert get_json(base+bridge)['release']['version']=='13.40-r93'
    pages=get_json(GH+WEB+'/actions/runs/'+str(closeout['pages_run']))
    assert pages['head_sha']==closeout['web_commit'] and pages['conclusion']=='success'
    for page in ('','gsu.html'):
        for retry in range(4):
            parser=Portal()
            parser.feed(fetch(SITE+page,1024*1024).decode('utf-8'))
            if release['url'] in parser.links and TAG in ''.join(parser.text):
                break
            if retry==3:
                raise ValueError('published portal is stale '+SITE+page)
            time.sleep(15)
        assert {'sk','en','de','ru'}<=parser.languages
        assertions=(('Diagnostické centrá','Diagnostic centres','Diagnosebereiche','Центры диагностики') if page else
                    ('Sedem centier pre stav prijímača','Seven centres cover receiver health','Sieben Bereiche bündeln Gerätestatus','Семь центров объединяют состояние ресивера'))
        assert all(fragment in ''.join(parser.text) for fragment in assertions)
        if page:
            assert release['release_url'] in parser.links and release['url']+'.sha256' in parser.links
    print('Verified release bytes, both migration branches, Pages deployment and public SK/EN/DE/RU portal')


if __name__=='__main__':
    main()
