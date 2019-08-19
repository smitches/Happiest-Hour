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

        doAsync {

            val barsJson = getBarsAPI()

            uiThread {
                val barList = getBarListFromJSONArray(barsJson)

                var adapter : BarCardListViewAdapter? = null
                adapter = BarCardListViewAdapter(requireActivity(), barList)
                view.bar_list_view.adapter = adapter
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

}