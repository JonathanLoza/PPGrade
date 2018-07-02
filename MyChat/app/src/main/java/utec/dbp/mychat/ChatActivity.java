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

public class ChatActivity extends AppCompatActivity {
    public static final String EXTRA_USER_ID = "userID";
    public static final String EXTRA_USER_NAME = "userFullname";
    public static final String TAG = "ChatActivity";

    RecyclerView mRecyclerView;
    RecyclerView.Adapter mAdapter;

    public Activity getActivity() {
        return this;
    }
    public void showMessage(String message) {
        Toast.makeText(this, message, Toast.LENGTH_LONG).show();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat);
        mRecyclerView = findViewById(R.id.main_recycler_view);
        final String userFullname = getIntent().getExtras().get(EXTRA_USER_NAME).toString();
        setTitle("Bienvenido "+userFullname);
    }

    @Override
    protected void onResume() {
        super.onResume();

        mRecyclerView.setLayoutManager(new LinearLayoutManager(this));
        final String userId = getIntent().getExtras().get(EXTRA_USER_ID).toString();
        String url = "http://10.0.2.2:5000/cursos/"+userId;
        RequestQueue queue = Volley.newRequestQueue(this);

        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(
            Request.Method.GET, url, null, new Response.Listener<JSONObject>() {
                @Override
                public void onResponse(JSONObject response) {
                    try {
                        mAdapter = new MyAdapter(response.getJSONArray("response"),getActivity(), userId);
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

        final EditText addcurso = (EditText) findViewById(R.id.addcurso);
        final String userId = getIntent().getExtras().get(EXTRA_USER_ID).toString();

        String url = "http://10.0.2.2:5000/addcurso";
        RequestQueue queue = Volley.newRequestQueue(this);

        Map<String, String> params = new HashMap();
        params.put("name", addcurso.getText().toString());
        params.put("user_id", userId);

        JSONObject parameters = new JSONObject(params);
        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest
                (Request.Method.POST, url, parameters, new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            if (response.getBoolean("response")) {
                                onResume();
                            } else {
                                showMessage("Error");
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                }, new Response.ErrorListener() {

                    @Override
                    public void onErrorResponse(VolleyError error) {
                        // TODO: Handle error
                        addcurso.setText("Response: " + error.toString());
                    }
                });
        queue.add(jsonObjectRequest);
    }
}