package com.example.happierhour

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import android.widget.ArrayAdapter
import android.widget.Spinner
import kotlinx.android.synthetic.main.add_review.view.*
import okhttp3.OkHttpClient
import org.jetbrains.anko.doAsync
import org.jetbrains.anko.info
import org.jetbrains.anko.uiThread
import org.json.JSONArray
import org.json.JSONObject
import kotlinx.android.synthetic.main.filter_hhs.*
import kotlinx.android.synthetic.main.filter_hhs.view.*
import kotlinx.android.synthetic.main.filter_hhs.view.button
import com.example.happierhour.MyApplication.Companion.filtered_hhs


class FilterHHsFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.filter_hhs, container, false)


        doAsync {
            val response = getRegions()
            println(response.toString())
            val jsonarray = JSONArray(response)
            uiThread {
                val region_names: ArrayList<String> = ArrayList()
                region_names.add("")
                for (i in 0..(jsonarray.length() - 1)) {
                    val region = jsonarray.getJSONObject(i)
                    region_names.add(region.get("region_name").toString())
                }

                val adapter =
                    ArrayAdapter<String>(requireActivity(), android.R.layout.simple_spinner_item, region_names)
                adapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line)
                SpinnerRegion.adapter = adapter
            }
        }

        doAsync {
            val response = getFeatures()
            println(response.toString())
            val jsonarray = JSONArray(response)
            uiThread {
                val feature_names: MutableList<String> = ArrayList()
                feature_names.add("")
                for (i in 0..(jsonarray.length() - 1)) {
                    val region = jsonarray.getJSONObject(i)
                    feature_names.add(region.get("feature_title").toString())
                }

                val adapter =
                    ArrayAdapter<String>(requireActivity(), android.R.layout.simple_spinner_item, feature_names)
                adapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line)
                SpinnerFeatures.adapter = adapter
            }
        }

        view.button.setOnClickListener {

            val selectedDay: String = SpinnerDay.selectedItem.toString()
            val selectedRegion: String = SpinnerRegion.selectedItem.toString()
            val selectedFeature: String = SpinnerFeatures.selectedItem.toString()

            val minStarCount: String = minStarCount.text.toString()
            val drinksDiscounted: Boolean = checkDrink.isChecked()
            val foodsDiscounted: Boolean = checkFood.isChecked()



            val contents: HashMap<String, String> = HashMap<String, String>()

            if (selectedDay != "") {
                var dayString: String = ""
                if (selectedDay == "Monday") {
                    dayString = "M"
                } else if (selectedDay == "Tuesday") {
                    dayString = "T"
                } else if (selectedDay == "Wednesday") {
                    dayString = "W"
                } else if (selectedDay == "Thursday") {
                    dayString = "Th"
                } else if (selectedDay == "Friday") {
                    dayString = "F"
                } else if (selectedDay == "Saturday") {
                    dayString = "Sa"
                } else if (selectedDay == "Tuesday") {
                    dayString = "Su"
                }
                contents.put("day", dayString)
            }

            if (selectedRegion != "") {

                //get region id
                doAsync {

                    val response = getRegions()
                    val jsonarray = JSONArray(response)

                    var regionId : String = ""
                    for (i in 0..(jsonarray.length() - 1)) {
                        val region = jsonarray.getJSONObject(i)
                        if (region.get("region_name") == selectedRegion) {
                            regionId = region.get("id").toString()
                        }
                    }

                    uiThread {
                        contents.put("region_id", regionId)
                    }

                }

            }

            if (selectedFeature != "") {

                //get feature id
                doAsync {
                    val response = getFeatures()
                    val jsonarray = JSONArray(response)

                    var featureId : String = ""
                    for (i in 0..(jsonarray.length() - 1)) {
                        val feature = jsonarray.getJSONObject(i)
                        if (feature.get("feature_name") == selectedFeature) {
                            featureId = feature.get("id").toString()
                        }
                    }

                    uiThread {
                        contents.put("feature_ids", "[{\"feature_id\":\"$featureId\"}]")
                    }

                }

            }

            if (minStarCount != "") {
                contents.put("star_count", minStarCount)

            }

            if (drinksDiscounted == true) {
                contents.put("drinks", "true")

            }

            if (foodsDiscounted == true) {
                contents.put("food", "true")

            }

            println(contents)

            doAsync {
                val responses = findHappyHours(contents)
                filtered_hhs = responses

                uiThread {

                    (activity as NavigationHost).navigateTo(HHsFilteredFragment(),addToBackstack = true)
                }
            }


        }
        return view
    }

        private fun getRegions(): String? {

            val client = OkHttpClient()
            val request = MyOkHttpRequest(client)

            val url = "http://happierhour.appspot.com/api/regions/"

            val response_body = request.GET(url)
            println(response_body)

            return response_body
        }

        private fun getFeatures(): String? {

            val client = OkHttpClient()
            val request = MyOkHttpRequest(client)

            val url = "http://happierhour.appspot.com/api/features/"

            val response_body = request.GET(url)

            return response_body
        }

        private fun findHappyHours(contents: HashMap<String, String>): String? {

            val client = OkHttpClient()
            val request = MyOkHttpRequest(client)

            val url = "http://happierhour.appspot.com/api/happyhours/search/"

            val response_body = request.POST(url, contents)

            return response_body
        }

    }