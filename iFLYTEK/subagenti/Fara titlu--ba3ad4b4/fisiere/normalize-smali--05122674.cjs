'use strict';
const crypto=require('node:crypto');
const sha=text=>crypto.createHash('sha256').update(text,'utf8').digest('hex');
const debug=/^\.(?:source\b|line\b|local\b|end local\b|restart local\b|prologue\b|epilogue\b)/;
const directive=/^\.(?:class|super|implements|field|method|registers|locals|param|annotation|subannotation|array-data|packed-switch|sparse-switch|catch|catchall|end)\b/;
function normalizeSmali(text){
 if(typeof text!=='string'||text.includes('\0'))throw Error('Invalid Smali text');
 const lines=[];for(const original of text.replace(/\r\n?/g,'\n').split('\n')){const s=original.trim();if(!s||s.startsWith('#')||debug.test(s))continue;if(s.startsWith('.')&&!directive.test(s))throw Error('Unknown Smali directive: '+s);if(s.startsWith('.end ')&&!/^\.end (?:field|method|param|annotation|subannotation|array-data|packed-switch|sparse-switch)$/.test(s))throw Error('Unknown Smali end directive: '+s);lines.push(s);}
 const declarations=lines.filter(s=>s.startsWith('.class '));if(declarations.length!==1)throw Error('Expected exactly one class declaration');
 const descriptor=declarations[0].match(/\s(L[^\s;]+;)$/)?.[1];if(!descriptor)throw Error('Invalid class descriptor');
 if(lines.filter(s=>s.startsWith('.super ')).length>1)throw Error('Ambiguous superclass');
 const methods=[],seen=new Set(),context=[];let current=null;
 for(const s of lines){
  if(s.startsWith('.method ')){if(current)throw Error('Nested method declaration');const [CREDENTIAL_REDACTED]\s([^\s]+\([^)]*\)[^\s]+)$/)?.[1];if(!signature)throw Error('Invalid method declaration');if(seen.has(signature))throw Error('Duplicate method descriptor: '+signature);seen.add(signature);current={signature,lines:[s]};}
  else if(s==='.end method'){if(!current)throw Error('Unmatched end method');current.lines.push(s);const normalized=current.lines.join('\n')+'\n';methods.push({descriptor:descriptor+'->'+current.signature,signature:current.signature,sha256:sha(normalized),bytes:Buffer.byteLength(normalized),normalized});current=null;}
  else if(current)current.lines.push(s);else context.push(s);
 }
 if(current)throw Error('Unterminated method');
 const normalized=lines.join('\n')+'\n',classContext=context.join('\n')+'\n';
 return {schemaVersion:1,normalization:'smali-conservative-v1',descriptor,classSha256:sha(normalized),contextSha256:sha(classContext),bytes:Buffer.byteLength(normalized),methodCount:methods.length,methods,normalized,classContext};
}
module.exports={normalizeSmali};
