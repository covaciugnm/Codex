const fs=require('fs'),cp=require('child_process'),p=require('path'),crypto=require('crypto');
const root='D:/CodexWork/eva-audit-p01-readonly-20261102',dir='Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/A02';const db=require(dir+'/CESIRO_metadate.json').data;const source=root+'/idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/corelare/RezervareStoc.java';const raw=fs.readFileSync(source,'utf8');
function constant(name,params){const m=raw.match(new RegExp('String '+name+' = ([\\s\\S]*?);'));if(!m)throw Error(name);let q=[...m[1].matchAll(/"([^"\\]*(?:\\.[^"\\]*)*)"/g)].map(x=>JSON.parse('"'+x[1]+'"')).join('');let i=0;q=q.replace(/\?/g,()=>params[i++]);if(i!==params.length)throw Error(name);return q;}
const index=t=>db.indexes.find(x=>x.index_name===t).definition.replace('ON adempiere.','ON ');
const stock=w=>`COALESCE((SELECT t.amount FROM (${constant('SQL_STOC',[1,1,w])}) t(wh,amount)),0)`,nr=w=>`(${constant('SQL_REZ_NATIVA',[1,1,w])})`,ar=`(${constant('SQL_REZ_T22',[1,1,"'R'",999])})`;
const query=`\\set ON_ERROR_STOP on
CREATE TABLE m_locator(m_locator_id int primary key,m_warehouse_id int not null);
CREATE TABLE m_storageonhand(ad_client_id int,m_product_id int,m_locator_id int,qtyonhand numeric);
CREATE TABLE m_storagereservation(ad_client_id int,m_product_id int,m_warehouse_id int,isactive char(1),issotrx char(1),qty numeric);
CREATE TABLE eva_comandasitelinie(ad_client_id int,m_product_id int,eva_starelinie text,m_inout_id int,eva_comandasite_id int,eva_cantitaterezervata numeric);
INSERT INTO m_locator VALUES(11,1),(22,2); INSERT INTO m_storageonhand VALUES(1,1,11,10),(1,1,22,10); INSERT INTO eva_comandasitelinie VALUES(1,1,'R',NULL,10,7);
SELECT json_build_object('id','R01-global','expected_total',13,'eva_warehouse_1',${stock(1)}-${nr(1)}-${ar},'eva_warehouse_2',${stock(2)}-${nr(2)}-${ar},'eva_sum_g1_net',(${stock(1)}-${nr(1)}-${ar})+(${stock(2)}-${nr(2)}-${ar}),'oracle',(${stock(1)}+${stock(2)}-${ar}));
DELETE FROM eva_comandasitelinie; INSERT INTO m_storagereservation VALUES(1,1,1,'Y','N',4),(1,1,1,'Y','Y',2);
SELECT json_build_object('id','R02-po-vs-so','onhand',${stock(1)},'native_reserved', (SELECT SUM(qty) FROM m_storagereservation WHERE issotrx='Y'),'native_ordered',(SELECT SUM(qty) FROM m_storagereservation WHERE issotrx='N'),'eva_nativa',${nr(1)},'eva_available',${stock(1)}-${nr(1)}-${ar},'oracle_native_available',8);
CREATE TABLE eva_stocwms(ad_client_id numeric(10) NOT NULL,m_locator_id numeric(10),m_product_id numeric(10),m_attributesetinstance_id numeric(10),pp_product_bom_id numeric(10),qty numeric);
${index('eva_stocwms_uk')}; INSERT INTO eva_stocwms VALUES(1,11,1,NULL,NULL,10),(1,11,1,NULL,NULL,10);
SELECT json_build_object('id','W01-null-unique','persisted_rows',count(*),'represented_qty',sum(qty),'expected_keys',1,'expected_physical_quantity',10) FROM eva_stocwms;
INSERT INTO eva_stocwms VALUES(1,11,2,0,0,1); INSERT INTO eva_stocwms VALUES(1,11,2,0,0,1) ON CONFLICT DO NOTHING;
SELECT json_build_object('id','W02-zero-unique','persisted_rows',count(*),'expected_rows',1) FROM eva_stocwms WHERE m_product_id=2;
INSERT INTO eva_stocwms VALUES(1,11,3,0,0,-4); SELECT json_build_object('id','W03-negative-db-guard','rows_with_negative_quantity',count(*)) FROM eva_stocwms WHERE qty<0;
CREATE TABLE m_product(m_product_id numeric(10) PRIMARY KEY,m_product_uu varchar(36),value varchar(40) NOT NULL,ad_client_id numeric(10) NOT NULL); ${db.indexes.filter(x=>x.table_name==='m_product'&&/\(m_product_uu\)|\(ad_client_id, value\)/i.test(x.definition)).map(x=>x.definition.replace('ON adempiere.','ON ')+';').join('\n')}
INSERT INTO m_product VALUES(1,'00000000-0000-0000-0000-000000000001','P001',1); DELETE FROM m_product WHERE m_product_id=1; INSERT INTO m_product VALUES(2,'00000000-0000-0000-0000-000000000002','P001',1); SELECT json_build_object('id','I01-reuse-value','value','P001','original_row_id',1,'new_row_id',m_product_id,'outcome','same business code accepted for a different identity by projected constraints') FROM m_product WHERE value='P001';
BEGIN; INSERT INTO eva_stocwms VALUES(1,11,99,0,0,9); ROLLBACK; SELECT json_build_object('id','TX01','remaining_rows_after_rollback',COUNT(*)) FROM eva_stocwms WHERE m_product_id=99;
CREATE TABLE lock_probe(id int PRIMARY KEY,qty int NOT NULL); INSERT INTO lock_probe VALUES(1,1);
CREATE TABLE dimensions(k int,qty int); INSERT INTO dimensions SELECT n,n%17 FROM generate_series(1,100000) n; CREATE INDEX dimensions_key ON dimensions(k); ANALYZE dimensions;
SELECT json_build_object('id','V01-fixture-volume','rows',count(*),'target',100000) FROM dimensions;
`;
const remote=`set -eu
queue=/home/saga-server/Documents/EvA-Contab/tools/status/coada_builduri.sh
slot=$("$queue" cere codex-a02-audit codex P01.T354 --tip suita --pid $$ --scop 'A02 audit PostgreSQL sintetic izolat, stoc si rezervari' ) || exit $?
container=''; cleanup(){ if [ -n "$container" ] && [ "$(docker inspect -f '{{index .Config.Labels "eva.audit.owner"}}' "$container" 2>/dev/null)" = 'codex-a02-20261102' ]; then docker rm -f -v "$container" >/dev/null; fi; "$queue" elibereaza "$slot" >&2; }
trap cleanup EXIT; trap 'exit 130' INT TERM
container=$(docker run --detach --network none --label eva.audit.owner=codex-a02-20261102 --tmpfs /var/lib/postgresql/data:rw,size=700m --memory=1000m --cpus=1.5 -e POSTGRES_HOST_AUTH_METHOD=trust postgres:16)
for n in $(seq 1 35); do docker exec "$container" pg_isready -U postgres >/dev/null 2>&1 && break; sleep 1; done
docker exec "$container" pg_isready -U postgres >/dev/null
docker inspect --format 'FIXTURE {{.Id}} {{.Config.Image}} {{.HostConfig.NetworkMode}}' "$container"
docker exec -i "$container" psql -X -qAt -v ON_ERROR_STOP=1 -U postgres -d postgres <<'AUDIT_SQL'
${query}
AUDIT_SQL
docker exec -i "$container" psql -X -qAt -v ON_ERROR_STOP=1 -U postgres -d postgres -c 'BEGIN; SELECT pg_advisory_xact_lock(12002); UPDATE lock_probe SET qty=qty-1 WHERE id=1 AND qty>=1; SELECT pg_sleep(1); COMMIT;' >/dev/null &
pa=$!; sleep 0.2
docker exec -i "$container" psql -X -qAt -v ON_ERROR_STOP=1 -U postgres -d postgres -c 'BEGIN; SELECT pg_advisory_xact_lock(12002); UPDATE lock_probe SET qty=qty-1 WHERE id=1 AND qty>=1; COMMIT;' >/dev/null &
pb=$!; wait "$pa"; wait "$pb"; docker exec -i "$container" psql -X -qAt -U postgres -d postgres -c "SELECT json_build_object('id','TX02-synthetic-lock','qty_after_two_consumers',qty,'expected',0) FROM lock_probe;"
docker exec -i "$container" psql -X -qAt -U postgres -d postgres -c 'EXPLAIN (ANALYZE ON, FORMAT JSON) SELECT qty FROM dimensions WHERE k=99000;' | tr '\n' ' ' | sed 's/^/PERF /'; echo
`;fs.writeFileSync(p.join(dir,'fixture_source.sql'), query);const run=cp.spawnSync('ssh',['-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','saga-server@192.168.100.151','bash -s'],{input:remote,encoding:'utf8',timeout:120000,maxBuffer:4*1024*1024});const lines=run.stdout.trim().split('\n');const results=lines.filter(x=>x.startsWith('{')).map(x=>JSON.parse(x));const ev={id:'EV-A02-PG-FIXTURE',utc:new Date().toISOString(),code_sha:'6df998aee0e514d30856c461962afe99ebd0d113',source:'corelare/RezervareStoc.java SQL_STOC/SQL_REZ_NATIVA/SQL_REZ_T22 extracted literally and instantiated with fixture arguments',source_sha256:crypto.createHash('sha256').update(raw).digest('hex'),source_script_sha256:crypto.createHash('sha256').update(query).digest('hex'),scope:'PostgreSQL 16 propriu fără rețea sau volum partajat; tabele sintetice, fără aplicație ERP. Indexurile EVA_StocWms și M_Product provin din metadatele CESIRO. Nu simulează validările PO. TX01/TX02/V01 demonstrează mecanismele fixture, nu un E2E de produs.',container:lines.find(x=>x.startsWith('FIXTURE')),exit:run.status,stderr:run.stderr.trim(),results,perf:JSON.parse((lines.find(x=>x.startsWith('PERF '))||'PERF null').slice(5)),cleanup:run.stderr.includes('eliberat:')&&run.status===0};fs.writeFileSync(p.join(dir,'PG_fixture_rezultate.json'),JSON.stringify(ev,null,2));console.log(JSON.stringify(ev));if(run.status!==0)process.exitCode=run.status||1;
