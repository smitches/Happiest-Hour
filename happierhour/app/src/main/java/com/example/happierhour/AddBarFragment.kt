package com.example.happierhour

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import kotlinx.android.synthetic.main.add_bar.*
import kotlinx.android.synthetic.main.add_bar.view.*
import org.json.JSONArray
import org.json.JSONObject
import android.R.string
import android.widget.ArrayAdapter
import kotlinx.android.synthetic.main.filter_hhs.*
import okhttp3.*
import org.jetbrains.anko.*
import org.json.JSONException
import java.io.IOException


class AddBarFragment : Fragment() {

    var RegionNameToId = HashMap<String, String>()
    var FeatureNameToId = HashMap<String, String>()

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.add_bar, container, false)

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
                    RegionNameToId.put(region.get("bar_name").toString(), region.get("id").toString())
                }

                val adapter =
                    ArrayAdapter<String>(requireActivity(), android.R.layout.simple_spinner_item, region_names)
                adapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line)
                SpinnerRegionbar.adapter = adapter
            }
        }

        doAsync {
            val response = getRegions()
            println(response.toString())
            val jsonarray = JSONArray(response)
            uiThread {
                val feature_names: ArrayList<String> = ArrayList()
                feature_names.add("")
                for (i in 0..(jsonarray.length() - 1)) {
                    val feature = jsonarray.getJSONObject(i)
                    feature_names.add(feature.get("feature_title").toString())
                    FeatureNameToId.put(feature.get("feature_title").toString(), feature.get("id").toString())
                }

                val adapter =
                    ArrayAdapter<String>(requireActivity(), android.R.layout.simple_spinner_item, feature_names)
                adapter.setDropDownViewResource(android.R.layout.simple_dropdown_item_1line)
                SpinnerFeaturesbar.adapter = adapter
            }
        }

        view.button.setOnClickListener {

            val nameInput: String = barNameEditText.text.toString()
            val addressInput: String = barAddressEditText.text.toString()
            val phoneInput: String = barPhoneEditText.text.toString()

            val selectedRegion: String = SpinnerRegionbar.selectedItem.toString()
            val selectedFeature: String = SpinnerFeaturesbar.selectedItem.toString()

            val contents: HashMap<String, String> = HashMap<String, String>()
            contents.put("bar_name", nameInput)
            contents.put("street_address", addressInput)
            contents.put("phone_number", phoneInput)
            contents.put("region", RegionNameToId.get(selectedRegion).toString())
            val featureId = FeatureNameToId.get(selectedRegion).toString()
            contents.put("features", "[{\"feature_id\":\"$featureId\"}]")


            doAsync {

                val postresponse = addInfo(contents)

                uiThread {

                    (activity as NavigationHost).navigateTo(ManageBarsFragment(), addToBackstack = false)

                }
            }

        }

        return view
    }

    private fun addInfo(contents: HashMap<String, String>): String? {

        val client = OkHttpClient()
        val request = MyOkHttpRequest(client)

        val url = "https://happierhour.appspot.com/api/reviews/create/"

        val response_body = request.POST(url, contents)

        println(response_body)

        return request.POST(url, contents)

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
        println(response_body)

        return response_body
    }
}

