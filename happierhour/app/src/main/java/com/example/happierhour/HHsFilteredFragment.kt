package com.example.happierhour

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import kotlinx.android.synthetic.main.hhs_filtered.*
import org.json.JSONArray
import com.example.happierhour.MyApplication.Companion.filtered_hhs

class HHsFilteredFragment() : Fragment() {

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {

        println(filtered_hhs)
        val view = inflater.inflate(R.layout.hhs_filtered, container, false)

        var adapter : MyHHAdapter? = null
        var hhList : ArrayList<HH_Model>
        hhList = generateHappyHourData()

        adapter = MyHHAdapter(requireActivity(), hhList)

        println(adapter == null)

        hh_list.adapter = adapter

//        list.setOnItemClickListener { adapterView, view, i, l ->
//            Toast.makeText(this, "Selected Emp is = "+ hhList.get(i).emp_name, Toast.LENGTH_SHORT).show()
//        }
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

        return result
    }

}
