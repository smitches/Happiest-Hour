package com.example.happierhour

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.example.happierhour.MyApplication.Companion.user
import com.example.happierhour.MyApplication.Companion.user_token
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
import kotlinx.android.synthetic.main.guest_landing_page.view.*
import kotlinx.android.synthetic.main.guest_landing_page.view.filterbutton
import kotlinx.android.synthetic.main.guest_landing_page.view.loginbutton
import kotlinx.android.synthetic.main.guest_landing_page.view.seeallbutton
import kotlinx.android.synthetic.main.login_landing_page.view.*
import kotlinx.android.synthetic.main.logout_fragment.view.*

class GuestLandingPageFragement(): Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        if (user_token != ""){
            val view = inflater.inflate(R.layout.login_landing_page,container,false)
            doAsync {
                user = logged_in_user()
                uiThread {
                    view.welcome_text.text = "WELCOME " + user.username
                }
            }
            view.logout_button.setOnClickListener {
                (activity as NavigationHost).navigateTo(LogoutFragment(), false)
            }

            view.filterbutton.setOnClickListener {
                (activity as NavigationHost).navigateTo(FilterHHsFragment(),addToBackstack = true)
            }

            view.seeallbutton.setOnClickListener {
                (activity as NavigationHost).navigateTo(SeeAllBarsFragment(),addToBackstack = true)
            }

            view.manage_bars_button.setOnClickListener {

                (activity as NavigationHost).navigateTo(ManageBarsFragment(),addToBackstack = true)
            }
            view.create_review_button.setOnClickListener {
                (activity as NavigationHost).navigateTo(AddReviewFragment(),addToBackstack = true)
            }
        }else{
            val view = inflater.inflate(R.layout.guest_landing_page, container, false)

            view.loginbutton.setOnClickListener {
                (activity as NavigationHost).navigateTo(LoginFragment(),addToBackstack = false)
            }

            view.filterbutton.setOnClickListener {
                (activity as NavigationHost).navigateTo(FilterHHsFragment(),addToBackstack = true)
            }

            view.seeallbutton.setOnClickListener {
                (activity as NavigationHost).navigateTo(SeeAllBarsFragment(),addToBackstack = true)
            }
        }

        return view
    }

    fun logged_in_user() : User_Model{
        val client = OkHttpClient()
        val request = MyOkHttpRequest(client)
        val url = "http://happierhour.appspot.com/api/whoami/"
        val response_body = request.GET(url)
        return getUserFromJSONObject(JSONArray(response_body).getJSONObject(0))
    }

}