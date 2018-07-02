package utec.dbp.mychat;

import android.app.Activity;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class MessageActivity extends AppCompatActivity {
    public static final String EXTRA_USER_ID = "user_id";
    public static final String EXTRA_CURSO_ID = "curso_id";
    public static final String EXTRA_CURSO_NAME = "curso_name";
    public static final String TAG = "MessageActivity";

    RecyclerView mRecyclerView;
    RecyclerView.Adapter mAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_message);
        mRecyclerView = findViewById(R.id.main_recycler_view);
        final String curso_name = getIntent().getExtras().get(EXTRA_CURSO_NAME).toString();
        setTitle(curso_name);
    }

    public Activity getActivity() {
        return this;
    }

    public void showMessage(String message) {
        Toast.makeText(this, message, Toast.LENGTH_LONG).show();
    }


    @Override
    protected void onResume() {
        super.onResume();
        mRecyclerView.setLayoutManager(new LinearLayoutManager(this));
        final String user_id = getIntent().getExtras().get(EXTRA_USER_ID).toString();
        final String curso_id = getIntent().getExtras().get(EXTRA_CURSO_ID).toString();
        String url = "http://10.0.2.2:5000/notas/"+curso_id;
        RequestQueue queue = Volley.newRequestQueue(this);

        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(
                Request.Method.GET, url, null, new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                try {
                    final String fin=response.getString("final");
                    TextView first_line=findViewById(R.id.fin);
                    first_line.setText(fin);
                    mAdapter = new MyMessageAdapter(response.getJSONArray("response"),getActivity(), Integer.parseInt(curso_id));
                    mRecyclerView.setAdapter(mAdapter);
                } catch (JSONException e) {
                    Log.d(TAG, e.getMessage());
                }
            }
        }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                Log.d(TAG, error.getMessage());
            }
        }
        );
        queue.add(jsonObjectRequest);
    }
    public void onClickBtnLogin(View v) {

        final EditText nota = (EditText) findViewById(R.id.notanueva);
        EditText variable = (EditText) findViewById(R.id.variable);
        EditText porcentaje = (EditText) findViewById(R.id.porcentaje);
        final String curso_id = getIntent().getExtras().get(EXTRA_CURSO_ID).toString();

        String url = "http://10.0.2.2:5000/addnota";
        RequestQueue queue = Volley.newRequestQueue(this);

        Map<String, String> params = new HashMap();
        params.put("nota", nota.getText().toString());
        params.put("variable", variable.getText().toString());
        params.put("porcentaje", porcentaje.getText().toString());
        params.put("curso_id", curso_id);

        JSONObject parameters = new JSONObject(params);
        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest
                (Request.Method.POST, url, parameters, new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            if (response.getBoolean("response")) {
                                onResume();
                            } else {
                                showMessage("Error de datso ingresados");
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                }, new Response.ErrorListener() {

                    @Override
                    public void onErrorResponse(VolleyError error) {
                        // TODO: Handle error
                        nota.setText("Response: " + error.toString());
                    }
                });
        queue.add(jsonObjectRequest);
    }
}
