package com.example.happierhour


import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import kotlinx.android.synthetic.main.display_reviews.*
import kotlinx.android.synthetic.main.display_reviews.view.*
import org.json.JSONArray
import org.json.JSONObject
import android.R.string
import okhttp3.*
import org.jetbrains.anko.*
import org.json.JSONException
import java.io.IOException


class SeeReviewFragment : Fragment(), AnkoLogger {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.display_reviews, container, false)

        view.button.setOnClickListener {
            info("good")
            doAsync {
                info("good2")
                val gotresponse = fetchInfo()
                val jsonarray = JSONArray(gotresponse)
                uiThread {

                   reviews.text = jsonarray.toString()
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

    private fun fetchInfo(): String? {

        val client = OkHttpClient()
        val request = MyOkHttpRequest(client)

        val url = "http://happierhour.appspot.com/api/reviews"

        return request.GET(url)

    }

}

