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
import com.example.happierhour.MyApplication.Companion.review_id
import kotlinx.android.synthetic.main.display_reviews.my_review_list
import kotlinx.android.synthetic.main.hhs_filtered.view.*
import okhttp3.*
import org.jetbrains.anko.*
import org.json.JSONException
import java.io.IOException


//getting all reviews for a user
class SeeReviewFragment : Fragment(), AnkoLogger {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.display_reviews, container, false)


        doAsync {

            val gotresponse = fetchReviews()
            val jsonarray = JSONArray(gotresponse)

            uiThread {

                var adapter : MyReviewAdapter? = null
                var reviewList = ArrayList<Review_Model>()

                val reviews_to_list = jsonarray

                for (i in 0..(reviews_to_list.length() - 1)) {
                    val reviewObj = reviews_to_list.getJSONObject(i)
                    var review: Review_Model = getReviewFromJSONObject(reviewObj)

                    reviewList.add(review)
                }

                adapter = MyReviewAdapter(requireActivity(), reviewList)

                println(adapter == null)

                view.my_review_list.adapter = adapter

                view.my_review_list.setOnItemClickListener { adapterView, view, i, l ->

                    review_id = reviewList.get(i).r_id.toInt()

                    (activity as NavigationHost).navigateTo(ReviewDeleteFragment(),addToBackstack = true)

                }

            }
        }

        return view
    }


    private fun fetchReviews(): String? {

        val client = OkHttpClient()
        val request = MyOkHttpRequest(client)

        val url = "http://happierhour.appspot.com/api/myreviews/"

        return request.GET(url)

    }

}

