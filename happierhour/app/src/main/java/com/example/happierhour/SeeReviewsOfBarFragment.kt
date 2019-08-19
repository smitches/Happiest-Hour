package com.example.happierhour

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.example.happierhour.MyApplication.Companion.bar_id
import kotlinx.android.synthetic.main.display_reviews.*
import kotlinx.android.synthetic.main.single_review.*
import okhttp3.OkHttpClient
import org.jetbrains.anko.doAsync
import org.jetbrains.anko.uiThread
import org.json.JSONArray

class SeeReviewsOfBarFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.see_bars_reviews, container, false)



        doAsync {

            val gotresponse = fetchReviews()
            val jsonarray = JSONArray(gotresponse)

            uiThread {

                var adapter : MyReviewAdapter? = null
                var reviewList = ArrayList<Review_Model>()

                val reviews_to_list = JSONArray(jsonarray)

                for (i in 0..(reviews_to_list.length() - 1)) {
                    val reviewObj = reviews_to_list.getJSONObject(i)
                    var review: Review_Model = getReviewFromJSONObject(reviewObj)

                    reviewList.add(review)
                }

                adapter = MyReviewAdapter(requireActivity(), reviewList)

                println(adapter == null)

                review_list.adapter = adapter
                lbl_bar_name.text = getReviewFromJSONObject(reviews_to_list.getJSONObject(1)).bar.bar_name

            }
        }

        return view
    }


    private fun fetchReviews(): String? {

        val client = OkHttpClient()
        val request = MyOkHttpRequest(client)

        val url = "http://happierhour.appspot.com/api/bar/$bar_id/reviews"

        return request.GET(url)

    }

}
