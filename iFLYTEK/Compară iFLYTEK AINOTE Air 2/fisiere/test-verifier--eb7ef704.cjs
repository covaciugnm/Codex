'use strict';
const assert=require('node:assert/strict');
const {normalizeSmali,normalizeAttrs}=require('./normalization.cjs');
const field='.field public static ready:Z';
assert.equal(normalizeSmali(field+' = false'),normalizeSmali(field));
assert.notEqual(normalizeSmali(field+' = true'),normalizeSmali(field));
assert.notEqual(normalizeSmali('.field public static n:I = 0x1'),normalizeSmali('.field public static n:I'));
const split=`.method public run()V
.registers 1
:try_start_0
invoke-static {}, Ltest/T;->a()V
:try_end_0
.catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0
.line 2
:try_start_1
invoke-static {}, Ltest/T;->b()V
:try_end_1
.catch Ljava/lang/Exception; {:try_start_1 .. :try_end_1} :catch_0
return-void
:catch_0
move-exception v0
return-void
.end method`;
const merged=split.replace(':try_end_0\n.catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0\n.line 2\n:try_start_1','.line 2').replaceAll('try_end_1','try_end_0').replaceAll('try_start_1','try_start_0');
assert.equal(normalizeSmali(split),normalizeSmali(merged));
assert.notEqual(normalizeSmali(split),normalizeSmali(merged.replace('Ltest/T;->b()V','Ltest/T;->c()V')));
assert.notEqual(normalizeSmali(split),normalizeSmali(merged.replace('Ljava/lang/Exception;','Ljava/lang/RuntimeException;')));
assert.notEqual(normalizeSmali(split),normalizeSmali(merged.replace(/\.catch[^\n]+\n/,'')));
const x='<attr name="mode"><enum name="a" value="0"/><enum name="b" value="1"/></attr>';
const y='<attr name="mode"><enum name="b" value="1"/><enum name="a" value="0"/></attr>';
assert.equal(normalizeAttrs(x),normalizeAttrs(y));
assert.notEqual(normalizeAttrs(x),normalizeAttrs(y.replace('value="1"','value="2"')));
console.log('PASS: 9 equivalence and deliberate-regression checks');
