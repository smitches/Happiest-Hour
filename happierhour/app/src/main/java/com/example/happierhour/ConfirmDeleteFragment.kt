package com.example.happierhour

import android.content.Context
import android.net.Uri
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import com.example.happierhour.MyApplication.Companion.hh_id
import kotlinx.android.synthetic.main.fragment_confirm_delete.view.*
import kotlinx.android.synthetic.main.logout_fragment.view.*
import okhttp3.OkHttpClient
import org.jetbrains.anko.AnkoLogger
import org.jetbrains.anko.doAsync
import org.jetbrains.anko.info
import org.jetbrains.anko.uiThread
import org.json.JSONObject

class ConfirmDeleteFragment : Fragment(), AnkoLogger {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.fragment_confirm_delete, container, false)
        // Set an error if the password is less than 8 characters.


        view.confirm_delete_button.setOnClickListener({
            doAsync {
                deleteHh()
                uiThread {
                    (activity as NavigationHost).navigateTo(GuestLandingPageFragement(), false)
                }

            }

        })
        return view
    }
    fun deleteHh(){
        val client = OkHttpClient()
        val request = MyOkHttpRequest(client)

        val url = "http://happierhour.appspot.com/api/happy_hour/$hh_id/delete/"

        val response_body = JSONObject(request.DELETE(url))

        println(response_body)
    }
}