package com.example.happierhour

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import kotlinx.android.synthetic.main.add_review.*
import kotlinx.android.synthetic.main.add_review.view.*
import org.json.JSONArray
import org.json.JSONObject
import android.R.string
import okhttp3.*
import org.jetbrains.anko.*
import org.json.JSONException
import java.io.IOException


class AddReviewFragment : Fragment(), AnkoLogger {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.add_review, container, false)

        view.button.setOnClickListener {
            info("good")
            doAsync {
                info("good2")
                val postresponse = addInfo()
                uiThread {


                }
            }

        }

        return view
    }

//    private fun fetchInfo(): String {
//        val url = "https://apad19.appspot.com/list/"
//
//        val client = OkHttpClient()
//        val request = Request.Builder()
//            .url(url)
////            .header("User-Agent", "Android")
//            .build()
//        val response = client.newCall(request).execute()
//        val bodystr =  response.body().string() // this can be consumed only once
//
//        return bodystr
//    }

    private fun addInfo(): String? {

        val client = OkHttpClient()
        val request = MyOkHttpRequest(client)

        val url = "http://happierhour.appspot.com/api/reviews/"
        val contents:HashMap<String,String> = HashMap<String,String>()
        contents.put("star_count", "2" )
        contents.put("review_text", "From Android")
        contents.put("reviewer", "3")
        contents.put("bar", "12")
//        val contents:HashMap<String,String> = HashMap<String,String>()
//        contents.put("username", "Madi" )
//        contents.put("password", "madipassword")

        val response_body = request.POST(url, contents)
        info(response_body)


        return request.POST(url, contents)

    }

}