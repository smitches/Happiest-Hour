package com.example.happierhour

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.core.view.get
import androidx.fragment.app.Fragment
import com.example.happierhour.MyApplication.Companion.bar_id
import com.example.happierhour.MyApplication.Companion.hh_id
import com.example.happierhour.MyApplication.Companion.myBarIds
import kotlinx.android.synthetic.main.see_bars_hh.*
import kotlinx.android.synthetic.main.see_bars_hh.view.*
import okhttp3.OkHttpClient
import org.jetbrains.anko.doAsync
import org.jetbrains.anko.uiThread
import org.json.JSONArray

class SeeHHsOfBarFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.see_bars_hh, container, false)
        println(12)
        doAsync {

            val gotresponse = fetchHHs()
            val jsonarray = JSONArray(gotresponse)

            uiThread {

                var adapter: MyHHAdapter? = null
                var List: ArrayList<HH_Model>
                List = generateHappyHourData(jsonarray)

                adapter = MyHHAdapter(requireActivity(), List)

                bar_hh_list.adapter = adapter
                if (bar_id in myBarIds){
                    bar_hh_list.setOnItemClickListener { adapterView, view, i, l ->
                        hh_id = List.get(i).hh_id.toInt()
                        (activity as NavigationHost).navigateTo(ConfirmDeleteFragment(), addToBackstack = true)
                    }
                }else {

                    bar_hh_list.setOnItemClickListener { adapterView, view, i, l ->

                        (activity as NavigationHost).navigateTo(BarLandingPageFragment(), addToBackstack = true)
                    }
                }


            }
        }

        return view

    }

    private fun fetchHHs(): String? {

        val client = OkHttpClient()
        val request = MyOkHttpRequest(client)

        val url = "http://happierhour.appspot.com/api/bars/$bar_id/happyhours/"

        return request.GET(url)

    }

    private fun generateHappyHourData(returned_hhs : JSONArray): ArrayList<HH_Model> {
        var result = ArrayList<HH_Model>()

        for (i in 0 until returned_hhs.length()) {
            val hh = getHHFromJSONObject(returned_hhs.getJSONObject(i))
            result.add(hh)
        }

        println(result)

        return result
    }
}
