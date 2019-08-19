package com.example.happierhour

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.example.happierhour.MyApplication.Companion.bar_id
import kotlinx.android.synthetic.main.add_review.view.*
import okhttp3.OkHttpClient
import org.jetbrains.anko.doAsync
import org.jetbrains.anko.info
import org.jetbrains.anko.uiThread
import org.json.JSONArray
import org.json.JSONObject
import com.google.gson.Gson
import com.google.gson.GsonBuilder
import com.google.gson.reflect.TypeToken
import kotlinx.android.synthetic.main.bar_landing_page.*
import kotlinx.android.synthetic.main.bar_landing_page.view.*
import kotlinx.android.synthetic.main.guest_landing_page.view.*

class BarLandingPageFragment(): Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.bar_landing_page, container, false)

        doAsync {

            val response = getHHs()
            val jsonarray = JSONArray(response)

            uiThread {
                val happyhour = jsonarray.getJSONObject(0)
                val menu = happyhour.get("menu_pdf").toString()

                view.menubutton.setOnClickListener {
                    val uri = Uri.parse(menu) // missing 'http://' will cause crashed
                    val intent = Intent(Intent.ACTION_VIEW, uri)
                    startActivity(intent)
                }

                barTextView.text = getHHFromJSONObject(happyhour).hh_bar.bar_name
            }
        }

        view.reviewbutton.setOnClickListener {
            (activity as NavigationHost).navigateTo(SeeReviewsOfBarFragment(),addToBackstack = true)
        }

        view.hhsbutton.setOnClickListener {
            (activity as NavigationHost).navigateTo(SeeHHsOfBarFragment(),addToBackstack = true)
        }

        return view
    }


    private fun getHHs(): String? {

        val client = OkHttpClient()
        val request = MyOkHttpRequest(client)

        val url = "http://happierhour.appspot.com/api/bar/$bar_id/happyhours"

        val response_body = request.GET(url)
        println(response_body)

        return response_body
    }

}