// Version-specific ARM64 patch for official libapp.so 1.0.3899, Dart 3.10.9.
// Dart registers: x15=SP, x22=null, x26=thread, x27=pool, x28=heap bits.
// All allocating calls retain existing caller PCs and existing stack maps.
// Helpers are leaf code, or tail calls. No custom Dart object headers or
// hand-managed allocations are introduced.
.arch armv8-a

.section .patch.0156cf14,"ax"
    mov x2, #16                 // Eight map literal entries (four key/value pairs).

.section .patch.0156cf3c,"ax"
    mov x16, #6                 // Smi(3): length of "+40".
    str x16, [x15]
    bl original_965844                 // allocateOneByteString, existing GC call site.
    b init_prefix

.section .patch.0156cfa8,"ax"
    mov x16, #14                // Smi(7): length of "Romania".
    str x16, [x15]
    bl original_965844                 // Existing GC call site.
    b init_label

.section .patch.01283120,"ax"
    b prepare_dropdown

.section .patch.01283150,"ax"
    b after_dropdown_map

.section .patch.01283158,"ax"
    bl dropdown_call           // Reuse the original SizeExtension.h call PC.
    b dropdown_call_return

.section .patch.0128390c,"ax"
    bl country_length

.section .patch.011184c4,"ax"
    bl country_length

.section .patch.00fa92d0,"ax"
    b validate_phone

.section .extension,"ax"
.balign 16
.global init_prefix, init_label, prepare_dropdown, dropdown_call
.global dropdown_call_return, after_dropdown_map, country_length, validate_phone

// Test an ASCII country prefix in x2. Only x16/x17 and condition flags change.
.macro branch_unless_ro destination
    ldur w16, [x2, #-1]
    ubfx w16, w16, #12, #20
    cmp w16, #94                // Dart OneByteString class, version pinned.
    b.ne \destination
    ldur w16, [x2, #7]
    cmp w16, #6                 // Smi(3).
    b.ne \destination
    ldur w16, [x2, #15]
    and w16, w16, #0x00ffffff
    movz w17, #0x342b
    movk w17, #0x30, lsl #16
    cmp w16, w17                // "+40" in little endian.
    b.ne \destination
.endm

init_prefix:
    movz w16, #0x342b
    movk w16, #0x30, lsl #16
    stur w16, [x0, #15]
    ldur x1, [x29, #-16]        // Existing rooted map literal array.
    add x25, x1, #0x27          // Element 6: key "+40".
    str w0, [x25]
    ldr x3, [x26, #0xa0]        // Immutable empty arguments for Intl._message.
    adr x30, prefix_done
    b array_barrier
prefix_done:
    b original_156cf4c                 // Original translated Chinese Mainland label.

init_label:
    movz x16, #0x6f52
    movk x16, #0x616d, lsl #16
    movk x16, #0x696e, lsl #32
    movk x16, #0x0061, lsl #48
    stur x16, [x0, #15]         // "Romania", including a zero padding byte.
    ldur x1, [x29, #-16]
    add x25, x1, #0x2b          // Element 7: label.
    str w0, [x25]
    ldr x3, [x26, #0xa0]
    adr x30, label_done
    b array_barrier
label_done:
    b original_156cfb8                 // Original translated Hong Kong label.

// Original Dart generational/incremental write barrier, including slow paths.
// This stub has no GC-capable calls (its native buffer helpers are leaf calls).
// Inputs: x0=value, x1=array, x25=slot. Preserves x0/x1/x3.
array_barrier:
    ldurb w16, [x1, #-1]
    ldurb w17, [x0, #-1]
    and x16, x17, x16, lsr #2
    tst x16, x28, lsr #32
    b.ne original_18a1330
    ret

prepare_dropdown:
    stur x0, [x29, #-0x20]      // Closure rooted where the list is normally rooted.
    str xzr, [x15]             // Smi phase 0, not a GC pointer.
    mov x1, #20                // Original Smi(10), passed unchanged to .h().
    b original_1283158

dropdown_call:
    ldr x16, [x15]
    cbnz x16, dropdown_allocate
    b original_9eea60                 // Preserve exact original screen scaling.
dropdown_allocate:
    b original_18a3084                // Dart AllocateArray; original caller PC retained.

dropdown_call_return:
    ldr x16, [x15]
    cbnz x16, fill_dropdown
    stur d0, [x29, #-0xa8]      // Existing unboxed double stack slot.
    mov x16, #2
    str x16, [x15]
    ldr x1, [x27, #0x5c8]      // TypeArguments<String>.
    mov x2, #8                 // Smi(4).
    b original_1283158                // Second allocation at the same registered PC.

fill_dropdown:
    add x16, x27, #0x3b, lsl #12
    ldr x17, [x16, #0xa10]
    stur w17, [x0, #0xf]        // +86
    ldr x17, [x16, #0xa20]
    stur w17, [x0, #0x13]       // +852
    add x16, x27, #0x50, lsl #12
    ldr x17, [x16, #0x7c0]
    stur w17, [x0, #0x17]       // +853
    ldur x16, [x29, #-8]        // Existing outer closure context.
    ldur w16, [x16, #0xf]       // _PhoneNumberInputer state.
    add x16, x16, x28, lsl #32
    ldur w16, [x16, #0x17]      // Country name map.
    add x16, x16, x28, lsl #32
    ldur w16, [x16, #0xf]       // Map insertion-ordered backing array.
    add x16, x16, x28, lsl #32
    ldur w17, [x16, #0x27]      // Fourth key, added by the constructor.
    add x17, x17, x28, lsl #32
    mov x1, x0
    mov x0, x17
    add x25, x1, #0x1b
    str w0, [x25]              // +40, with normal write barrier.
    adr x30, dropdown_ready
    b array_barrier
dropdown_ready:
    mov x30, x1
    add x16, x27, #0x5d, lsl #12
    ldr x16, [x16, #0xdc8]     // TypeArguments<DropdownMenuItem<String>>.
    ldur x0, [x29, #-0x20]
    b original_1283130                // Original ListBase.map and GrowableList.of.

after_dropdown_map:
    stur x0, [x29, #-0x20]
    ldur d0, [x29, #-0xa8]
    fneg d1, d0
    b original_1283160

country_length:
    branch_unless_ro existing_country_length
    mov x0, #18                // Smi(9): national significant number length.
    ret
existing_country_length:
    b original_179f91c                // Original three-country lookup.

validate_phone:
    branch_unless_ro existing_phone_validation
    ldur w16, [x1, #-1]
    ubfx w16, w16, #12, #20
    cmp w16, #94
    b.ne phone_invalid
    ldur w16, [x1, #7]
    cmp w16, #18
    b.ne phone_invalid
    ldurb w16, [x1, #15]
    cmp w16, #0x37             // Romanian mobile number begins with 7 after +40.
    b.ne phone_invalid
    add x3, x1, #15
    mov x4, #9
phone_digits:
    ldrb w16, [x3], #1
    sub w16, w16, #0x30
    cmp w16, #9
    b.hi phone_invalid
    subs x4, x4, #1
    b.ne phone_digits
    add x0, x22, #0x20         // Dart true.
    ret
phone_invalid:
    add x0, x22, #0x30         // Dart false.
    ret
existing_phone_validation:
    stp x29, x30, [x15, #-0x10]!
    b original_fa92d4                 // Original prologue/validation for other countries.
