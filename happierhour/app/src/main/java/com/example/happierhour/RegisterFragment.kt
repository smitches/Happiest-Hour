package com.example.happierhour

import android.content.Context
import android.net.Uri
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import kotlinx.android.synthetic.main.fragment_register.*
import kotlinx.android.synthetic.main.fragment_register.view.*
import com.google.gson.GsonBuilder


import android.text.Editable
import com.google.gson.reflect.TypeToken
import okhttp3.OkHttpClient
import org.jetbrains.anko.AnkoLogger
import org.jetbrains.anko.doAsync
import org.jetbrains.anko.info
import org.jetbrains.anko.uiThread
import org.json.JSONArray
import org.json.JSONObject

/**
 * Fragment representing the login screen for Shrine.
 */
class RegisterFragmentFragment : Fragment(), AnkoLogger {
    var body = HashMap<String, String>()
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.fragment_register, container, false)
        // Set an error if the password is less than 8 characters.
        view.register_button.setOnClickListener({
            if (!isPasswordValid(password1_edit_text.text!!)) {
                password1_text_input.error = getString(R.string.error_password)
            } else {
                // Clear the error.
                password1_text_input.error = null
                // Navigate to the next Fragment
            }
            body.set("username",username_edit_text.text.toString())
            body.set("email",email_edit_text.text.toString())
            body.set("password1",password1_edit_text.text.toString())
            body.set("password2",password2_edit_text.text.toString())
            info(body.toString())
            status_text.text = "Pending"
            doAsync {
                info("calling API")
                val apiresponse = fetchInfo()
                info(apiresponse.toString())
                val jsonobj = JSONObject(apiresponse)
                info(jsonobj.toString())
                uiThread {
                    status_text.text = jsonobj.toString()
                }
//                info(jsonobj.keys())
//                info(jsonobj.has("username"))
                if(jsonobj.has("key")){
                    info("does have that key")
                    (activity as NavigationHost).navigateTo(AddReviewFragment(), false)
                }
//                var gson = GsonBuilder().create()
//                var userStringList: List<String> = gson.fromJson(jsonobj.get("username"), object : TypeToken<List<String>>)
//                gson.fromJson()
//
            }
            //username android_user
            //password Twbmpwfma
        })

        // Clear the error once more than 8 characters are typed.
        view.password1_edit_text.setOnKeyListener({ _, _, _ ->
            if (isPasswordValid(password1_edit_text.text!!)) {
                // Clear the error.
                password1_text_input.error = null
            }
            false
        })
        return view
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

    private fun fetchInfo(): String? {

        val client = OkHttpClient()
        val request = MyOkHttpRequest(client)

        val url = "http://happierhour.appspot.com/api/rest-auth/registration/"

        return request.POST(url, body)

    }

}




//// TODO: Rename parameter arguments, choose names that match
//// the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
//private const val ARG_PARAM1 = "param1"
//private const val ARG_PARAM2 = "param2"
//
///**
// * A simple [Fragment] subclass.
// * Activities that contain this fragment must implement the
// * [RegisterFragment.OnFragmentInteractionListener] interface
// * to handle interaction events.
// * Use the [RegisterFragment.newInstance] factory method to
// * create an instance of this fragment.
// *
// */
//class RegisterFragment : Fragment() {
//    // TODO: Rename and change types of parameters
//    private var param1: String? = null
//    private var param2: String? = null
//    private var listener: OnFragmentInteractionListener? = null
//
//    override fun onCreate(savedInstanceState: Bundle?) {
//        super.onCreate(savedInstanceState)
//        arguments?.let {
//            param1 = it.getString(ARG_PARAM1)
//            param2 = it.getString(ARG_PARAM2)
//        }
//    }
//
//    override fun onCreateView(
//        inflater: LayoutInflater, container: ViewGroup?,
//        savedInstanceState: Bundle?
//    ): View? {
//        // Inflate the layout for this fragment
//        return inflater.inflate(R.layout.fragment_register, container, false)
//    }
//
//    // TODO: Rename method, update argument and hook method into UI event
//    fun onButtonPressed(uri: Uri) {
//        listener?.onFragmentInteraction(uri)
//    }
//
//    override fun onAttach(context: Context) {
//        super.onAttach(context)
//        if (context is OnFragmentInteractionListener) {
//            listener = context
//        } else {
//            throw RuntimeException(context.toString() + " must implement OnFragmentInteractionListener")
//        }
//    }
//
//    override fun onDetach() {
//        super.onDetach()
//        listener = null
//    }
//
//    /**
//     * This interface must be implemented by activities that contain this
//     * fragment to allow an interaction in this fragment to be communicated
//     * to the activity and potentially other fragments contained in that
//     * activity.
//     *
//     *
//     * See the Android Training lesson [Communicating with Other Fragments]
//     * (http://developer.android.com/training/basics/fragments/communicating.html)
//     * for more information.
//     */
//    interface OnFragmentInteractionListener {
//        // TODO: Update argument type and name
//        fun onFragmentInteraction(uri: Uri)
//    }
//
//    companion object {
//        /**
//         * Use this factory method to create a new instance of
//         * this fragment using the provided parameters.
//         *
//         * @param param1 Parameter 1.
//         * @param param2 Parameter 2.
//         * @return A new instance of fragment RegisterFragment.
//         */
//        // TODO: Rename and change types and number of parameters
//        @JvmStatic
//        fun newInstance(param1: String, param2: String) =
//            RegisterFragment().apply {
//                arguments = Bundle().apply {
//                    putString(ARG_PARAM1, param1)
//                    putString(ARG_PARAM2, param2)
//                }
//            }
//    }
//}
