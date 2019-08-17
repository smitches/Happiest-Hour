//package com.example.happierhour
//
//import android.os.Bundle
//import android.view.LayoutInflater
//import android.view.View
//import android.view.ViewGroup
//import androidx.fragment.app.Fragment
//import kotlinx.android.synthetic.main.add_review.view.*
//import okhttp3.OkHttpClient
//import org.jetbrains.anko.doAsync
//import org.jetbrains.anko.info
//import org.jetbrains.anko.uiThread
//import org.json.JSONArray
//import org.json.JSONObject
//import com.google.gson.Gson
//import com.google.gson.GsonBuilder
//import com.google.gson.reflect.TypeToken
//
//class LandingPageFragement(val username: String, val password: String, val token: String): Fragment() {
//
//    override fun onCreateView(
//        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
//        // Inflate the layout for this fragment
//        val view = inflater.inflate(R.layout.add_review, container, false)
//
//        doAsync {
//            val user = getUser(token)
//            val jsonobject= JSONObject(user)
//
//            //convert jsonobject string into class user
//
//
//        }
//
//        view.button.setOnClickListener {
//            doAsync {
//                val postresponse = addInfo()
//            }
//
//        }
//
//        return view
//    }
//
//    private fun getUser(token: String): String? {
//
//        val client = OkHttpClient()
//        val request = MyOkHttpRequest(client)
//
//        val url  = "https://happierhour.appspot.com/api/whoami/"
//
//        val response_body = request.GET(url)
//
//        return response_body
//
//    }
//
//}