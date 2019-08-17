package com.example.happierhour

import java.util.HashMap

import okhttp3.FormBody
import okhttp3.MediaType
import okhttp3.OkHttpClient
import okhttp3.Request


class MyOkHttpRequest(client: OkHttpClient) {
    internal var client = OkHttpClient()

    init {
        this.client = client
    }

   val mytoken = "01a9f063a216f68483c45cf0bbe584bd7de109ac"

    fun POST(url: String, parameters: HashMap<String, String>) : String? {
        val builder = FormBody.Builder()
        val it = parameters.entries.iterator()
        while (it.hasNext()) {
            val pair = it.next() as Map.Entry<*, *>
            builder.add(pair.key.toString(), pair.value.toString())
        }

       val formBody = builder.build()
       val request = Request.Builder()
            .url(url)
//            .header("Authorization", "Token $mytoken")
            .post(formBody)
            .build()


        val response = client.newCall(request).execute()
        val bodystr = response.body()?.string()
        return bodystr
    }

    fun GET(url: String): String? {
        val request = Request.Builder()
            .url(url)
            .header("Authorization", "Token $mytoken")
            .build()

        val response = client.newCall(request).execute()
        val bodystr = response.body()?.string()
        return bodystr
    }

    companion object {
        val JSON = MediaType.parse("application/json; charset=utf-8")
    }
}