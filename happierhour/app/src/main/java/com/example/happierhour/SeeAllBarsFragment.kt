package com.example.happierhour

import android.app.Activity
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import androidx.fragment.app.Fragment
import kotlinx.android.synthetic.main.login_fragment.view.*
import kotlinx.android.synthetic.main.see_bars.*
import kotlinx.android.synthetic.main.see_bars.view.*
import okhttp3.OkHttpClient
import org.jetbrains.anko.AnkoLogger
import org.jetbrains.anko.doAsync
import org.jetbrains.anko.info
import org.jetbrains.anko.uiThread
import org.json.JSONArray

class SeeAllBarsFragment : Fragment(), AnkoLogger {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.see_bars, container, false)

//        view.next_button.setOnClickListener {
//
//        }
        info(1)
        doAsync {

            info(2)
            val barsJson = getBarsAPI()

            uiThread {
                var barListView = view.bar_list_view
                info(3)
                val barList = getBarListFromJSONArray(barsJson)
                info(4)
                val listItems = mutableListOf<String>()
                info(5)
                for (i in 0 until barList.size) {
                    val bar = barList[i]
                    info(6)
                    listItems.add(bar.bar_name)
                }
                info(7)
                info(barList)


                info(8)
                val myContext = context!!
                info(myContext)
                info(android.R.layout.simple_list_item_1)
                info(listItems)
//                val adapter = ArrayAdapter<String>(myContext,android.R.layout.simple_list_item_1,listItems)
//                barListView.adapter = adapter
                var adapter : BarCardListViewAdapter? = null
//                adapter = BarCardListViewAdapter(myContext as Activity, barList)
                adapter = BarCardListViewAdapter(requireActivity(), barList)

                bar_list_view.adapter = adapter
                info(9)
            }

        }
        return view
    }
    fun getBarsAPI() : JSONArray{
        val client = OkHttpClient()
        val request = MyOkHttpRequest(client)

        val url = "http://happierhour.appspot.com/api/bars/"
        info("a")
        val resp = request.GET(url)
        info("b")
        val jarray = JSONArray(resp)
        info("c")
        return jarray
    }
    fun getBarListFromJSONArray(jsonArrayInput:JSONArray): ArrayList<Bar_Model> {
        val size = jsonArrayInput.length()
        var barList = ArrayList<Bar_Model>()
        for (i in 0 until size){
            val barJson = jsonArrayInput.getJSONObject(i)
            val feature_json_array = barJson.getJSONArray("features")
            var feature_list = mutableListOf<Int>()
            for (i in 0 until feature_json_array.length()){
                feature_list.add(feature_json_array.get(i).toString().toInt())
            }
            val bar = Bar_Model(
                barJson.get("id").toString().toInt(),
                barJson.get("bar_name").toString(),
                barJson.get("street_address").toString(),
                barJson.get("phone_number").toString(),
                barJson.get("approved").toString() == "true" || barJson.get("approved").toString() == "True",
                barJson.get("region").toString().toInt(),
                barJson.get("region").toString().toInt(),
                feature_list
            )
            barList.add(bar)
        }
        return barList
    }
}