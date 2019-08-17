package com.example.happierhour

import android.os.Bundle
import android.text.Editable
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import kotlinx.android.synthetic.main.fragment_register.view.*
import kotlinx.android.synthetic.main.login_fragment.*
import kotlinx.android.synthetic.main.login_fragment.view.*
import org.json.JSONArray
import org.json.JSONObject
import com.google.gson.Gson
import com.google.gson.GsonBuilder
import com.google.gson.reflect.TypeToken
import okhttp3.OkHttpClient
import org.jetbrains.anko.doAsync
import org.jetbrains.anko.info

/**
 * Fragment representing the login screen for Shrine.
 */
class LoginFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.login_fragment, container, false)
        // Set an error if the password is less than 8 characters.
        view.next_button.setOnClickListener({
            if (!isPasswordValid(password_edit_text.text!!)) {
                password_text_input.error = "Password needs to be 8 characters or more."
            } else {
                //clear the error
                password_text_input.error = null

                // Navigate to the next Fragment.
                (activity as NavigationHost).navigateTo(SeeReviewFragment(), false)


                doAsync {
                    val usernameInput = username_edit_text.getText().toString()
                    val passwordInput = password_edit_text.getText().toString()
                    val getTheToken = checkLoginIn(usernameInput, passwordInput)
                    println(getTheToken)
                    if (getTheToken != null) {
                        (activity as NavigationHost).navigateTo(AddReviewFragment(), false)
                    }
                }
            }
        })
        view.sign_up_button.setOnClickListener({
            (activity as NavigationHost).navigateTo(RegisterFragmentFragment(),addToBackstack = false)
        })

        // Clear the error once more than 8 characters are typed.
        view.password_edit_text.setOnKeyListener({ _, _, _ ->
            if (isPasswordValid(password_edit_text.text!!)) {
                // Clear the error.
                password_text_input.error = null
            }
            false
        })
        return view
    }

    private fun checkLoginIn(username: String, password: String) : String {

        val client = OkHttpClient()
        val request = MyOkHttpRequest(client)

        val url = "http://happierhour.appspot.com/api/rest-auth/login/"

        val contents:HashMap<String,String> = HashMap<String,String>()
        contents.put("username", "$username" )
        contents.put("password", "$password")

        val response_body = JSONObject(request.POST(url, contents))

        val returnedToken = response_body.get("key").toString()
        println(returnedToken)

        return returnedToken
    }

    // "isPasswordValid"  method goes here
    // Currently checks for 8 characters but we could perform
    // an actual validation with a remote service like the Web version below
    private fun isPasswordValid(text: Editable?): Boolean {
        return text != null && text.length >= 8
    }

    private fun isPasswordValidWeb(text: Editable?): Boolean {
        return true
    }

}
