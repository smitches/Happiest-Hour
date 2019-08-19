package com.example.happierhour

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
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

class GuestLandingPageFragement(): Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.guest_landing_page, container, false)

        view.filterbutton.setOnClickListener {
            (activity as NavigationHost).navigateTo(FilterHHsFragment(),addToBackstack = true)
        }

        view.seeallbutton.setOnClickListener {
            (activity as NavigationHost).navigateTo(SeeAllBarsFragment(),addToBackstack = true)
        }

        view.loginbutton.setOnClickListener {
            (activity as NavigationHost).navigateTo(LoginFragment(),addToBackstack = false)
        }

        return view
    }

}