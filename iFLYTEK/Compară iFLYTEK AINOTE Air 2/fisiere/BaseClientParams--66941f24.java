package translate_sdk;

import androidx.annotation.Keep;
import com.alipay.verifyiotidentity.obfuscated.rw5;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/* JADX INFO: loaded from: classes6.dex */
@Keep
public class BaseClientParams {
    public String cid;
    public String cloneid;
    public String deviceId;
    public String dstLang;
    public Map<String, Object> extraParams;
    public String hostId;
    public Boolean hotwordEnabled;
    public List<String> hotwordIds;
    public boolean isSave;
    public List<String> itshotwordIds;
    public boolean lastSession;
    public Map<String, Object> livereqparam;
    public String mVersion;
    public int mode;
    public String path;
    public String recordId;
    public Map<String, Object> rightparam;
    public boolean roleseparate;
    public String session;
    public String speakergender;
    public String speed;
    public String srcLang;
    public String srcVoiceName;
    public boolean supportsWorkBuddy;
    public String token;
    public String traceId;
    public String[] translator;
    public String uid;
    public String voiceName;
    public int devicetype = 0;
    public int scene = 0;
    public boolean resSpeex = false;
    public boolean support8xCompression = false;
    public boolean agsIntentEnabled = false;
    public boolean senstReturnError = false;
    public Map<String, Object> llmtransparam = new HashMap();
    public boolean autodirection = false;
    public boolean transdirection = false;

    public boolean getExtraBoolean(String str) {
        Map<String, Object> map = this.extraParams;
        if (map == null || !map.containsKey(str)) {
            return false;
        }
        Object obj = this.extraParams.get(str);
        if (obj instanceof Boolean) {
            return ((Boolean) obj).booleanValue();
        }
        return false;
    }

    public String getExtraValue(String str) {
        Map<String, Object> map = this.extraParams;
        if (map != null && map.containsKey(str) && (this.extraParams.get(str) instanceof String)) {
            return (String) this.extraParams.get(str);
        }
        return null;
    }

    public String toString() {
        return "BaseClientParams{uid='" + this.uid + "', session='" + this.session + "', traceId='" + this.traceId + "', speed='" + this.speed + "', voiceName='" + this.voiceName + "', srcVoiceName='" + this.srcVoiceName + "', path='" + this.path + "', token='" + this.token + "', hostId='" + this.hostId + "', extraParams=" + this.extraParams + ", recordId='" + this.recordId + "', isSave=" + this.isSave + ", lastSession=" + this.lastSession + ", livereqparam=" + this.livereqparam + ", rightparam=" + this.rightparam + ", srcLang='" + this.srcLang + "', dstLang='" + this.dstLang + "', mode=" + this.mode + ", deviceId='" + this.deviceId + "', cloneid='" + this.cloneid + "', translator=" + Arrays.toString(this.translator) + ", roleseparate=" + this.roleseparate + ", scene=" + this.scene + ", resSpeex=" + this.resSpeex + ", support8xCompression=" + this.support8xCompression + ", senstReturnError=" + this.senstReturnError + ", speakergender='" + this.speakergender + "', llmtransparam=" + this.llmtransparam + ", cid='" + this.cid + "', autodirection=" + this.autodirection + rw5.b;
    }
}
