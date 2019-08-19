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
import kotlinx.android.synthetic.main.display_reviews.review_list
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

                var adapter : MyHHAdapter? = null
                var reviewList : ArrayList<Review_Model>

                val reviews_to_list = JSONArray(MyApplication.filtered_hhs)

                for (i in 0..(reviews_to_list.length() - 1)) {
                    val reviewObj = reviews_to_list.getJSONObject(i)
                    var review: Review_Model = Review_Model(reviewObj.get("id").toString(),
                        reviewObj.getJSONObject("reviewer"), reviewObj.getJSONObject("bar"),
                        reviewObj.get("star_count").toString(), reviewObj.get("review_text").toString())

                    reviewList.add(review)
                }

                adapter = MyHHAdapter(requireActivity(), reviewList)

                println(adapter == null)

                review_list.adapter = adapter

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

