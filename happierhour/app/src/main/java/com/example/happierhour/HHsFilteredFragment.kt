package com.example.happierhour

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import com.example.happierhour.MyApplication.Companion.bar_id
import kotlinx.android.synthetic.main.hhs_filtered.*
import org.json.JSONArray
import com.example.happierhour.MyApplication.Companion.filtered_hhs
import kotlinx.android.synthetic.main.hhs_filtered.view.*
import kotlinx.android.synthetic.main.see_bars_hh.*

class HHsFilteredFragment() : Fragment() {

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {

        println(filtered_hhs)
        val view = inflater.inflate(R.layout.hhs_filtered, container, false)

        var adapter : MyHHAdapter? = null
        var List : ArrayList<HH_Model>
        List = generateHappyHourData()

        adapter = MyHHAdapter(requireActivity(), List)

        view.hh_list.adapter = adapter

        view.hh_list.setOnItemClickListener { adapterView, view, i, l ->

            bar_id = List.get(i).hh_bar.id_input.toInt()

            (activity as NavigationHost).navigateTo(BarLandingPageFragment(),addToBackstack = true)

        }
        return view
    }

    private fun generateHappyHourData(): ArrayList<HH_Model> {
        var result = ArrayList<HH_Model>()

        val hhs_to_list = JSONArray(filtered_hhs)

        for (i in 0 until hhs_to_list.length()) {
            val hh = getHHFromJSONObject(hhs_to_list.getJSONObject(i))
            result.add(hh)
        }

        filtered_hhs = ""

        println(result)

        return result
    }

}
