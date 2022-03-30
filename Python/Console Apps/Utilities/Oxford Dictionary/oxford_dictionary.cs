using System;

public class Program {
  public static void Main() {
    const string word_id = "swimming";
    const string lang_code = "en-us";
    const string fields = "pronunciations";
    const string strictMatch = "false";
    string WEBSERVICE_URL = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + lang_code + '/' + word_id + "?fields=" + fields + "&strictMatch=" + strictMatch;
    try {
        var webRequest = System.Net.WebRequest.Create(WEBSERVICE_URL);
        if (webRequest != null) {
            webRequest.Method = "GET";
            webRequest.Timeout = 12000;
            webRequest.ContentType = "application/json";
            webRequest.Headers.Add("app_id", "b7f6f8c8");
            webRequest.Headers.Add("app_key", "9d6a59520c16040983c8ff1be3b77a4c");

            using(System.IO.Stream s = webRequest.GetResponse().GetResponseStream()) {
              using(System.IO.StreamReader sr = new System.IO.StreamReader(s)) {
                var jsonResponse = sr.ReadToEnd();
                Console.WriteLine(String.Format("Response: {0}", jsonResponse));
              }
            }
        }
    } catch (Exception ex) {
        Console.WriteLine(ex.ToString());
    }
  }
}