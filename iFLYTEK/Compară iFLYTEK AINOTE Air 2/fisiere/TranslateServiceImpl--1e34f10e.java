package com.iflytek.fanyi.blc.service.impl;

import com.alipay.verifyiotidentity.obfuscated.i58;
import com.alipay.verifyiotidentity.obfuscated.j58;
import com.alipay.verifyiotidentity.obfuscated.jr9;
import com.alipay.verifyiotidentity.obfuscated.k36;
import com.iflytek.fanyi.blc.service.bean.AIHelperRequest;
import com.iflytek.fanyi.blc.service.bean.AIHelperResponse;
import com.iflytek.fanyi.blc.service.bean.AISummaryRequest;
import com.iflytek.fanyi.blc.service.bean.AISummaryResponse;
import com.iflytek.fanyi.blc.service.bean.AudioTransRequest;
import com.iflytek.fanyi.blc.service.bean.AudioTransResponse;
import com.iflytek.fanyi.blc.service.bean.AuthTransRequest;
import com.iflytek.fanyi.blc.service.bean.AuthTransResponse;
import com.iflytek.fanyi.blc.service.bean.ImageTransRequest;
import com.iflytek.fanyi.blc.service.bean.ImageTransResponse;
import com.iflytek.fanyi.blc.service.bean.ImmersiveAudioTransRequest;
import com.iflytek.fanyi.blc.service.bean.ImmersiveAudioTransResponse;
import com.iflytek.fanyi.blc.service.bean.LongAudioTransRequest;
import com.iflytek.fanyi.blc.service.bean.LongAudioTransResponse;
import com.iflytek.fanyi.blc.service.bean.TTSRequest;
import com.iflytek.fanyi.blc.service.bean.TTSResponse;
import com.iflytek.fanyi.blc.service.bean.TxtTransRequest;
import com.iflytek.fanyi.blc.service.bean.TxtTransResponse;
import io.grpc.CallOptions;
import io.grpc.Metadata;
import io.grpc.MethodDescriptor;
import java.lang.ref.SoftReference;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.Executor;

/* JADX INFO: loaded from: classes5.dex */
public class TranslateServiceImpl implements jr9 {
    private static Map<String, SoftReference<MethodDescriptor>> sCacheDescriptors;
    private Executor mExecutor;
    private j58 mTransport;

    public TranslateServiceImpl(j58 j58Var, Executor executor) {
        this.mTransport = j58Var;
        this.mExecutor = executor;
    }

    private static synchronized <Req, Resp> MethodDescriptor<Req, Resp> buildDescriptor(String str, Class<Req> cls, Class<Resp> cls2) {
        MethodDescriptor<Req, Resp> methodDescriptorBuild;
        try {
            if (sCacheDescriptors == null) {
                sCacheDescriptors = new HashMap();
            }
            SoftReference<MethodDescriptor> softReference = sCacheDescriptors.get(str);
            methodDescriptorBuild = softReference != null ? softReference.get() : null;
            if (methodDescriptorBuild == null) {
                methodDescriptorBuild = MethodDescriptor.newBuilder().setType(MethodDescriptor.MethodType.UNKNOWN).setFullMethodName(str).setRequestMarshaller(new k36(cls)).setResponseMarshaller(new k36(cls2)).build();
                sCacheDescriptors.put(str, new SoftReference<>(methodDescriptorBuild));
            }
        } catch (Throwable th) {
            throw th;
        }
        return methodDescriptorBuild;
    }

    @Override // com.alipay.verifyiotidentity.obfuscated.jr9
    public i58<AIHelperRequest, AIHelperResponse> createAIHelperTransStream(String str) {
        return this.mTransport.e(buildDescriptor(str, AIHelperRequest.class, AIHelperResponse.class), new Metadata(), CallOptions.DEFAULT, this.mExecutor);
    }

    @Override // com.alipay.verifyiotidentity.obfuscated.jr9
    public i58<AISummaryRequest, AISummaryResponse> createAISummaryTransStream(String str) {
        return this.mTransport.e(buildDescriptor(str, AISummaryRequest.class, AISummaryResponse.class), new Metadata(), CallOptions.DEFAULT, this.mExecutor);
    }

    @Override // com.alipay.verifyiotidentity.obfuscated.jr9
    public i58<AudioTransRequest, AudioTransResponse> createAudioTransStream(String str) {
        return this.mTransport.e(buildDescriptor(str, AudioTransRequest.class, AudioTransResponse.class), new Metadata(), CallOptions.DEFAULT, this.mExecutor);
    }

    @Override // com.alipay.verifyiotidentity.obfuscated.jr9
    public i58<AuthTransRequest, AuthTransResponse> createAuthTransStream(String str, String str2) {
        MethodDescriptor methodDescriptorBuildDescriptor = buildDescriptor(str, AuthTransRequest.class, AuthTransResponse.class);
        Metadata metadata = new Metadata();
        metadata.put(Metadata.Key.of("X-sign", Metadata.ASCII_STRING_MARSHALLER), str2);
        return this.mTransport.e(methodDescriptorBuildDescriptor, metadata, CallOptions.DEFAULT, this.mExecutor);
    }

    @Override // com.alipay.verifyiotidentity.obfuscated.jr9
    public i58<ImageTransRequest, ImageTransResponse> createImageTransStream(String str) {
        return this.mTransport.e(buildDescriptor(str, ImageTransRequest.class, ImageTransResponse.class), new Metadata(), CallOptions.DEFAULT, this.mExecutor);
    }

    @Override // com.alipay.verifyiotidentity.obfuscated.jr9
    public i58<ImmersiveAudioTransRequest, ImmersiveAudioTransResponse> createImmersiveAudioTransStream(String str) {
        return this.mTransport.e(buildDescriptor(str, ImmersiveAudioTransRequest.class, ImmersiveAudioTransResponse.class), new Metadata(), CallOptions.DEFAULT, this.mExecutor);
    }

    @Override // com.alipay.verifyiotidentity.obfuscated.jr9
    public i58<LongAudioTransRequest, LongAudioTransResponse> createLongAudioTransStream(String str) {
        return this.mTransport.e(buildDescriptor(str, LongAudioTransRequest.class, LongAudioTransResponse.class), new Metadata(), CallOptions.DEFAULT, this.mExecutor);
    }

    @Override // com.alipay.verifyiotidentity.obfuscated.jr9
    public i58<TTSRequest, TTSResponse> createTTSStream(String str) {
        return this.mTransport.e(buildDescriptor(str, TTSRequest.class, TTSResponse.class), new Metadata(), CallOptions.DEFAULT, this.mExecutor);
    }

    @Override // com.alipay.verifyiotidentity.obfuscated.jr9
    public i58<TxtTransRequest, TxtTransResponse> createTxtTransStream(String str) {
        return this.mTransport.e(buildDescriptor(str, TxtTransRequest.class, TxtTransResponse.class), new Metadata(), CallOptions.DEFAULT, this.mExecutor);
    }
}
