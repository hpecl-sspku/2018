#include <iostream>
#include <string>
#include <stdlib.h>
using namespace std;
#if 0
static int ReadLabelsFile(const char* labels_file, vector<string>* result)
{
    ifstream fs(labels_file);
    if(!fs)
    {
        cout << labels_file << " does not exist" << endl;
        return -1;
    }

    result->clear();
    string line;
    while(getline(fs, line))
    {
        result->push_back(line);
    }

    return 0;
}

static TF_Session* LoadGraph(const char* model_file, TF_Graph* graph)
{
    TF_Status* s = TF_NewStatus();

    vector<char> model_buf;

    if(ReadEntireFile(model_file, model_buf) < 0)
        return nullptr;

    TF_Buffer graph_def = {model_buf.data(), model_buf.size(), nullptr};

    TF_ImportGraphDefOptions* import_opts = TF_NewImportGraphDefOptions();
    TF_ImportGraphDefOptionsSetPrefix(import_opts, "");
    TF_GraphImportGraphDef(graph, &graph_def, import_opts, s);

    if(TF_GetCode(s) != TF_OK)
    {
        printf("load graph failed!\n Error: %s\n", TF_Message(s));
        return nullptr;
    }

    TF_SessionOptions* sess_opts = TF_NewSessionOptions();
    TF_Session* session = TF_NewSession(graph, sess_opts, s);
    assert(TF_GetCode(s) == TF_OK);

    TF_DeleteStatus(s);

    return session;
}

static int PrintTopLabels(const vector<TF_Tensor*>& outputs, const char* labels_file)
{
    vector<string> labels;
    int read_labels_status = ReadLabelsFile(labels_file, &labels);
    if(read_labels_status < 0)
        return -1;

    int label_count = labels.size();
    int N = std::min<int>(label_count, 5);

    float* data = ( float* )TF_TensorData(outputs[0]);

    vector<pair<int, float>> scores;
    for(int i = 0; i < label_count; i++)
    {
        scores.push_back(pair<int, float>({i, data[i]}));
    }

    sort(scores.begin(), scores.end(),
         [](const pair<int, float>& left, const pair<int, float>& right) { return left.second > right.second; });

    for(int pos = 0; pos < N; pos++)
    {
        const int label_index = scores[pos].first;
        const float score = scores[pos].second;
        cout << std::fixed << std::setprecision(4) << score << " - \"" << labels[label_index] << "\"" << endl;
    }
    return 0;
}
#endif
int main(int argc, char* argv[])
{
    if(!argv[1]){
      cout<<"You should input Temperature"<<endl;
      return -1;
    }
    
    if(!argv[2]){
      cout<<"You should input Humidity"<<endl;    
      return -1;
    }
    
    string str = argv[1];
    int T=atoi(str.c_str());
    int result = 0;
    
    //cout << "SmartHome" << endl;
#if 0
    vector<TF_Output> input_names;
    vector<TF_Tensor*> input_values;

    TF_Operation* input_name = TF_GraphOperationByName(graph, input_layer.c_str());
    input_names.push_back({input_name, 0});

    const int64_t dim[4] = {1, input_height, input_width, 3};

    TF_Tensor* input_tensor = TF_NewTensor(TF_FLOAT, dim, 4, input_data, sizeof(float) * input_height * input_width * 3,
                                           dummy_deallocator, nullptr);
    input_values.push_back(input_tensor);

    // Get output value
    vector<TF_Output> output_names;

    TF_Operation* output_name = TF_GraphOperationByName(graph, output_layer.c_str());
    output_names.push_back({output_name, 0});

    vector<TF_Tensor*> output_values(output_names.size(), nullptr);

    // Actually run the image through the model
    TF_Status* s = TF_NewStatus();
    TF_SessionRun(session, nullptr, input_names.data(), input_values.data(), input_names.size(), output_names.data(),output_values.data(), output_names.size(), nullptr, 0, nullptr, s);

    // Do something interesting with the results we've generated
    cout << "---------- Prediction for " << image_file << " ----------" << endl;
#endif
    if(T>25){result = 1;    }
    else if(T<15){result = 2;    }
    else{result = 3;    }
    
    
    if(result ==1){cout<<"1"<<endl;
      return 1;    }
    else if(result == 2){cout<<"2"<<endl;
      return 2;    }
    else{cout<<"0"<<endl;
      return 3;    }
    return 0;
}
