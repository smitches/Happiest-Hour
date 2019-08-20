package com.example.happierhour

import android.os.Bundle
import android.text.Editable
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.example.happierhour.MyApplication.Companion.user
import com.example.happierhour.MyApplication.Companion.user_token
import kotlinx.android.synthetic.main.logout_fragment.*
import kotlinx.android.synthetic.main.logout_fragment.view.*
import okhttp3.OkHttpClient
import org.jetbrains.anko.AnkoLogger
import org.jetbrains.anko.doAsync
import org.jetbrains.anko.info
import org.jetbrains.anko.uiThread
import org.json.JSONArray
import org.json.JSONObject

class LogoutFragment : Fragment(), AnkoLogger {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.logout_fragment, container, false)
        // Set an error if the password is less than 8 characters.
        doAsync {
            val username = getUsername()
            uiThread {
                view.logout_text.text = "Click to logout, " + username
            }

        }

        view.confirm_logout_button.setOnClickListener({
            doAsync {
                logoutAPI()
                (activity as NavigationHost).navigateTo(LoginFragment(), false)
            }

        })
        return view
    }
    fun getUsername() :  String{
        return user.username
    }
    fun logoutAPI(){
        val client = OkHttpClient()
        val request = MyOkHttpRequest(client)

        val url = "http://happierhour.appspot.com/api/rest-auth/logout/"

        val contents:HashMap<String,String> = HashMap<String,String>()
        contents.put("key", user_token )
        val response_body = JSONObject(request.POST(url, contents))

        info(response_body)

    }
}