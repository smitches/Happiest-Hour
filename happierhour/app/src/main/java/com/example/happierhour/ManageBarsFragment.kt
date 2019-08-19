package com.example.happierhour

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import androidx.fragment.app.Fragment
import com.example.happierhour.MyApplication.Companion.user
import kotlinx.android.synthetic.main.add_review.*
import kotlinx.android.synthetic.main.add_review.view.*
import kotlinx.android.synthetic.main.login_landing_page.view.*
import kotlinx.android.synthetic.main.manage_bars.view.*
import kotlinx.android.synthetic.main.see_bars.view.*
import okhttp3.OkHttpClient
import org.jetbrains.anko.doAsync
import org.jetbrains.anko.uiThread
import org.json.JSONArray

class ManageBarsFragment : Fragment() {
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {

        val view = inflater.inflate(R.layout.manage_bars, container, false)
        view.manage_text.text = view.manage_text.text + ": " + user.username
        var barList = ArrayList<Bar_Model>()
        view.bar_list_view.setOnItemClickListener { adapterView, view, i, l ->
            MyApplication.bar_id = barList[i].id_input.toInt()
            (activity as NavigationHost).navigateTo(BarLandingPageFragment(), false)
        }

        doAsync {

            val barsJson = getBarsAPI()

            uiThread {
                barList = getBarListFromJSONArray(barsJson)

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
        val url = "http://happierhour.appspot.com/api/mybars/"
        val resp = request.GET(url)
        val jarray = JSONArray(resp)

        return jarray
    }
}
