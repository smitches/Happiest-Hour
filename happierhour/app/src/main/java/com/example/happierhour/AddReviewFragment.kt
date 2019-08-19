package com.example.happierhour

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import kotlinx.android.synthetic.main.add_review.*
import kotlinx.android.synthetic.main.add_review.view.*
import org.json.JSONArray
import org.json.JSONObject
import android.R.string
import android.widget.ArrayAdapter
import kotlinx.android.synthetic.main.filter_hhs.*
import okhttp3.*
import org.jetbrains.anko.*
import org.json.JSONException
import java.io.IOException


class AddReviewFragment : Fragment() {

    var barNameToId = HashMap<String,String>()

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.add_review, container, false)

        doAsync {
            val response = getBars()
            println(response.toString())
            val jsonarray = JSONArray(response)
            uiThread {
                val bar_names: ArrayList<String> = ArrayList()
                bar_names.add("")
                for (i in 0..(jsonarray.length() - 1)) {
                    val bar = jsonarray.getJSONObject(i)
                    bar_names.add(bar.get("bar_name").toString())
                    barNameToId.put(bar.get("bar_name").toString(), bar.get("id").toString())
                }

                val adapter =
                    ArrayAdapter<String>(requireActivity(), android.R.layout.simple_spinner_item, bar_names)
                adapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line)
                SpinnerBars.adapter = adapter
            }
        }

        view.button.setOnClickListener {

            val selectedBar: String = SpinnerBars.selectedItem.toString()
            val selectedRating: String = SpinnerStar.selectedItem.toString()

            val writtenReview: String = EditTextReviewBody.text.toString()

            val contents:HashMap<String,String> = HashMap<String,String>()
            contents.put("star_count", selectedRating)
            contents.put("review_text", writtenReview)
            contents.put("bar", barNameToId.get(selectedBar).toString() )

            doAsync {

                val postresponse = addInfo(contents)

                uiThread {

                    (activity as NavigationHost).navigateTo(SeeReviewFragment(),addToBackstack = false)

                }
            }

        }

        return view
    }

    private fun addInfo(contents: HashMap<String, String>): String? {

        val client = OkHttpClient()
        val request = MyOkHttpRequest(client)

        val url  = "https://happierhour.appspot.com/api/reviews/create/"

        val response_body = request.POST(url, contents)

        println(response_body)

        return request.POST(url, contents)

    }

    private fun getBars(): String? {

        val client = OkHttpClient()
        val request = MyOkHttpRequest(client)

        val url = "http://happierhour.appspot.com/api/bars/"

        val response_body = request.GET(url)
        println(response_body)

        return response_body
    }

}