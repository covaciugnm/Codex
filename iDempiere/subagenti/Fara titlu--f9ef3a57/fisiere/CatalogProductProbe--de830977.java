import java.nio.file.*;
import java.util.*;
import java.io.*;
import com.google.gson.*;
import com.eva.ro.webshop.data.CatalogIndex;
import com.eva.ro.webshop.data.CatalogSource;
import com.eva.ro.webshop.data.JsonCatalogSource;
import com.eva.ro.webshop.store.StoreConfig;

public final class CatalogProductProbe {
    static final Gson GSON=new Gson();
    static void emit(String kind,Object value){System.out.println(kind+"|"+GSON.toJson(value));}
    static List<String> ids(List<?> items){
        List<String> result=new ArrayList<>();
        for(Object item:items)result.add(String.valueOf(((Map<?,?>)item).get("id")));
        return result;
    }
    static StoreConfig store(String tenant){
        return new StoreConfig(700001,700001,tenant,"synthetic.invalid","staging.synthetic.invalid","synthetic",List.of("ro"),"ro","RON",StoreConfig.DataSource.JSON);
    }
    public static void run(String laboratory) throws Exception {
        Path lab=Path.of(laboratory);
        CatalogIndex valid=CatalogIndex.build(lab.resolve("fixture/tenants/valid/catalog.json"));
        CatalogIndex empty=CatalogIndex.build(lab.resolve("fixture/tenants/empty/catalog.json"));
        if(valid.totalProducts()!=3||empty.totalProducts()!=0)throw new AssertionError("Original index fixture counts");
        List<String> originalIds=new ArrayList<>();for(CatalogIndex.Light p:valid.products())originalIds.add(String.valueOf(p.get("id")));
        if(!originalIds.equals(List.of("P1","P2","P3")))throw new AssertionError("Original index fixture identities");
        emit("INDEX_WITNESS",Map.of("valid_total",valid.totalProducts(),"valid_ids",originalIds,"empty_total",empty.totalProducts(),"empty_constructed",empty!=null,"absent_readable",Files.isReadable(lab.resolve("fixture/tenants/absent/catalog.json"))));
        JsonArray cases=JsonParser.parseString(Files.readString(lab.resolve("fixture/cases.json"))).getAsJsonArray();
        int count=0;
        for(JsonElement element:cases){
            JsonObject c=element.getAsJsonObject();String id=c.get("id").getAsString();String entry=c.get("entry").getAsString();
            int page=c.get("page_input").getAsInt(),per=c.get("per_page_input").getAsInt();
            Map<String,Object> result=new LinkedHashMap<>();result.put("id",id);result.put("entry",entry);result.put("page_input",page);result.put("per_page_input",per);
            try {
                JsonCatalogSource source=new JsonCatalogSource();StoreConfig config=store(c.get("tenant_fixture").getAsString());
                if(entry.equals("query")){
                    Map<String,Object> actual=source.queryProducts(config,"ro",null,null,page,per,"",Map.of());
                    result.put("outcome","RETURN");result.put("full_result",actual);result.put("product_ids",ids((List<?>)actual.get("items")));
                    result.put("total",actual.get("total"));result.put("page",actual.get("page"));result.put("per_page",actual.get("per_page"));result.put("has_more",actual.get("has_more"));
                }else{
                    CatalogSource.Page actual=source.listProducts(config,new CatalogSource.ProductQuery("ro",Map.of(),"",page,per));
                    result.put("outcome","RETURN");result.put("full_products",actual.products());result.put("product_ids",ids(actual.products()));
                    result.put("total",actual.total());result.put("page",actual.page());result.put("per_page",actual.pageSize());
                }
            } catch (Throwable ex){
                StringWriter sw=new StringWriter();ex.printStackTrace(new PrintWriter(sw));
                result.put("outcome","THROW");result.put("exception_class",ex.getClass().getName());result.put("exception_message",ex.getMessage());result.put("stacktrace",sw.toString());
                emit("CASE",result);count++;
                if(ex instanceof SecurityException || ex instanceof LinkageError)throw new AssertionError("Infrastructure failure at "+id,ex);
                if(id.equals("Q01"))throw new AssertionError("Positive baseline failed",ex);
                continue;
            }
            emit("CASE",result);count++;
            if(id.equals("Q01")&&(!result.get("product_ids").equals(List.of("P1","P2"))||((Number)result.get("total")).intValue()!=3))throw new AssertionError("Positive baseline incorrect");
        }
        if(count!=16)throw new AssertionError("Case count "+count);
        emit("DONE",Map.of("cases",count,"policy_active",System.getSecurityManager()!=null));
    }
}
