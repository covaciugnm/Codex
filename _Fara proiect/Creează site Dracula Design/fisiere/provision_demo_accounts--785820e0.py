"""Provision explicitly requested demo accounts. Password arrives through environment only."""
import os
from sqlalchemy import create_engine,text
from sqlalchemy.orm import Session
from app.security import hash_password
from app.repositories.identity_repo import IdentityRepo
from app.db import set_session_context
assert os.environ.get('COMMERCE_MODE')=='demo','Demo accounts must not be provisioned in live mode'
password=os.environ['DEMO_ACCOUNT_PASSWORD']
slug=os.environ['DEFAULT_TENANT'];domain=slug+'.com'
admin_email='admin@'+domain;client_email='client@'+domain
engine=create_engine(os.environ['SUPERUSER_DATABASE_URL'])
with Session(engine) as s,s.begin():
    tid=s.execute(text('SELECT id FROM core.tenants WHERE slug=:s'),{'s':slug}).scalar_one()
    set_session_context(s,tenant_id=str(tid),admin='on')
    admin_id=s.execute(text('SELECT id FROM identity.admin_users WHERE lower(email)=:e'),{'e':admin_email}).scalar()
    if admin_id is None:
        admin_id=s.execute(text("INSERT INTO identity.admin_users(email,full_name,password_hash,status,is_superadmin,must_change_password) VALUES(:e,:name,:p,'active',false,false) RETURNING id"),{'e':admin_email,'name':slug+' administrator test','p':hash_password(password)}).scalar_one()
    s.execute(text("INSERT INTO identity.admin_tenant_roles(admin_user_id,tenant_id,role) VALUES(:u,:t,'owner') ON CONFLICT(admin_user_id,tenant_id) DO UPDATE SET role='owner'"),{'u':admin_id,'t':tid})
    client=s.execute(text('SELECT id FROM identity.users WHERE tenant_id=:t AND lower(email)=:e'),{'t':tid,'e':client_email}).scalar()
    if client is None:
        IdentityRepo(s,str(tid)).register(email=client_email,password=password,full_name=slug+' client test',registration_source='admin')
        client=s.execute(text('SELECT id FROM identity.users WHERE tenant_id=:t AND email=:e'),{'t':tid,'e':client_email}).scalar_one()
        IdentityRepo(s,str(tid)).mark_email_verified(str(client))
print('Demo accounts ready:',admin_email,client_email)
