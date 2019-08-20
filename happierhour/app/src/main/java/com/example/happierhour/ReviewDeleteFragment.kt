package com.example.happierhour

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.example.happierhour.MyApplication.Companion.review_id
import kotlinx.android.synthetic.main.delete_review.view.*
import okhttp3.OkHttpClient
import org.jetbrains.anko.doAsync

class ReviewDeleteFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.delete_review, container, false)

        view.deleteText.text = "Would you like to delete this review?"

        view.button.setOnClickListener {

            doAsync {

                val response = deleteReview()
            }

            (activity as NavigationHost).navigateTo(SeeReviewFragment(),addToBackstack = true)
        }

        return view
    }

    private fun deleteReview(): String? {

        val client = OkHttpClient()
        val request = MyOkHttpRequest(client)

        val url = "http://happierhour.appspot.com/api/review/$review_id/delete/"

        val response_body = request.GET(url)

        println(response_body)

        return response_body
    }

}