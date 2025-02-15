package com.example.happierhour

import com.example.happierhour.MyApplication.Companion.user_token
import java.util.HashMap

import okhttp3.FormBody
import okhttp3.MediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import org.jetbrains.anko.AnkoLogger
import org.jetbrains.anko.info


class MyOkHttpRequest(client: OkHttpClient) : AnkoLogger {
    internal var client = OkHttpClient()

    init {
        this.client = client
    }



    fun POST(url: String, parameters: HashMap<String, String>) : String? {
        val builder = FormBody.Builder()
        val it = parameters.entries.iterator()
        while (it.hasNext()) {
            val pair = it.next() as Map.Entry<*, *>
            builder.add(pair.key.toString(), pair.value.toString())
        }

        val formBody = builder.build()
        var request : Request
        if (user_token!=""){
            request = Request.Builder()
                .url(url)
                .addHeader("Authorization", "Token $user_token")
//                .addHeader("content-type", "application/json")
                .post(formBody)
                .build()
        }else{
            request = Request.Builder()
                .url(url)
                .post(formBody)
                .build()
        }


        val response = client.newCall(request).execute()
        val bodystr = response.body()?.string()
        return bodystr
    }

    fun GET(url: String): String? {
        var request : Request

        if (user_token!="") {
            info("has user token")
            request = Request.Builder()
                .url(url).get()
                .addHeader("Authorization", "Token $user_token")
//                .addHeader("content-type", "application/json")
                .build()
        }else{
            info("no user token")
            info(url)
            request = Request.Builder()
                .url(url).get()
                .build()
        }
        val response = client.newCall(request).execute()
        println(url)
        println("about to call")
        val bodystr = response.body()?.string()
        println("body"+ bodystr)
        return bodystr
    }
    fun DELETE(url: String): String? {
        var request : Request

        if (user_token!="") {
            info("has user token")
            request = Request.Builder()
                .url(url).delete()
                .addHeader("Authorization", "Token $user_token")
//                .addHeader("content-type", "application/json")
                .build()
        }else{
            info("no user token")
            info(url)
            request = Request.Builder()
                .url(url).delete()
                .build()
        }
        println(request.toString())
        println(url)
        val response = client.newCall(request).execute()
        println(response)
        val bodystr = response.body()?.string()
        println(bodystr)
        return bodystr
    }


    companion object {
        val JSON = MediaType.parse("application/json; charset=utf-8")
    }
}