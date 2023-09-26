<template>
  <div class="home">
    <el-row id="" display="margin-top:10px">
      <el-input id="newId" v-model="input7" placeholder="请输入病人病历ID"
        style="display:inline-table; width: 12%; float:left"></el-input>
      <el-input id="newName" v-model="input1" placeholder="请输入病人姓名"
        style="display:inline-table; width: 12%; float:left"></el-input>
      <div id="step3" style="float:left;">
        <el-button type="primary" @click="save_patient()" style="float:left; margin: 2px;">新增</el-button>
      </div>
    </el-row>
    <el-row display="margin-top:10px">
      <el-input id="newUrl" v-model="input2" placeholder="结束录制后，请在此输入病人ID编号"
        style="display:inline-table; width: 18%; float:left"></el-input>
      <div id="step5" style="float:left;">
        <el-button type="primary" @click="update_patient()" style="float:left; margin: 2px;">添加视频url</el-button>
      </div>
    </el-row>
    <el-row display="margin-top:10px">
      <el-input id="query" v-model="input3" placeholder="请输入病人姓名"
        style="display:inline-table; width: 12%; float:right"></el-input>
      <div id="step6" style="float:right;">
        <el-button type="primary" @click="inquire_patient()" style="float:right; margin: 2px;">查询指定条目</el-button>
      </div>
    </el-row>
    <div id="step2">
      <img :src="ImageUrl" controls width="640" height="360" alt="实时视频流" title="实时摄像头画面">
    </div>
    <el-row display="margin-top:10px">
      <div id="step1" style="float:left;">
        <el-button type="primary" @click="start_camera()" style="float:left; margin: 2px;">打开摄像头</el-button>
      </div>
    </el-row>
    <el-row display="margin-top:10px">
      <div id="step12" style="float:left;">
        <el-button type="primary" @click="stop_camera()" style="float:left; margin: 2px;">关闭摄像头</el-button>
      </div>
    </el-row>
    <el-row display="margin-top:10px">
      <div id="step4" style="float:left;">
        <el-button type="primary" @click="start_record()" style="float:left; margin: 2px;">开启录制</el-button>
      </div>
    </el-row>
    <el-row>
      <el-dialog :visible.sync="dialogVisible1" title="提示" class="custom-dialog">
        <p>正在录制</p>
        <p>点击结束录制按钮停止录制</p>
        <div slot="footer" class="dialog-footer">
          <el-button type="primary" @click="stop_record">结束录制</el-button>
        </div>
      </el-dialog>
    </el-row>
    <!--
<el-row display="margin-top:10px">
<el-button type="primary" @click="stop_record()" style="float:left; margin: 2px;">结束录制</el-button>
</el-row>
-->
    <el-row display="margin-top:10px">
      <el-input id="query" v-model="input5" placeholder="请输入病人ID编号"
        style="display:inline-table; width: 12%; float:right"></el-input>
      <el-input id="query" v-model="input6" placeholder="请输入病人病种"
        style="display:inline-table; width: 12%; float:right"></el-input>
      <div id="step7" style="float:right;">
        <el-button type="primary" @click="disease_kind()" style="float:right; margin: 2px;">添加病人病种</el-button>
      </div>
    </el-row>
    <el-row display="margin-top:10px">
      <div id="step8" style="float:right;">
        <el-button type="primary" @click="upload_images()" style="float:right; margin: 2px;">同步本地图片</el-button>
      </div>
      <el-dialog title="提示" :visible="dialogVisible">
        <span>程序正在运行，请稍后...</span>
      </el-dialog>
    </el-row>
    <div id="step9">
      <el-row>
        <el-table :data="thePatient" stripe style="width: 100%" border max-height="1000">
          <el-table-column sortable prop="patientId" label="病历ID" min-width="100">
            <template v-slot="scope"> {{ scope.row.pk }} </template>
          </el-table-column>
          <el-table-column prop="patientName" label="病人姓名" min-width="100">
            <template v-slot="scope"> {{ scope.row.fields.patientName }} </template>
          </el-table-column>
          <el-table-column prop="diseaseKind" label="病种" min-width="100">
            <template v-slot="scope"> {{ scope.row.fields.diseaseKind }} </template>
          </el-table-column>
          <el-table-column prop="videoUrl" label="视频url" min-width="100">
            <template v-slot="scope"> {{ scope.row.fields.videoUrl }} </template>
          </el-table-column>
          <el-table-column prop="faceUrlSelf" label="面象url" min-width="100">
            <template v-slot="scope"> {{ scope.row.fields.faceUrlSelf }} </template>
          </el-table-column>
          <el-table-column prop="tongueUrlSelf" label="舌象url" min-width="100">
            <template v-slot="scope"> {{ scope.row.fields.tongueUrlSelf }} </template>
          </el-table-column>
          <el-table-column prop="faceUrlStd" label="基准面象url" min-width="100">
            <template v-slot="scope"> {{ scope.row.fields.faceUrlStd }} </template>
          </el-table-column>
          <el-table-column prop="tongueUrlStd" label="基准舌象url" min-width="100">
            <template v-slot="scope"> {{ scope.row.fields.tongueUrlStd }} </template>
          </el-table-column>
          <el-table-column prop="createTime" label="添加时间" min-width="100">
            <template v-slot="scope"> {{ scope.row.fields.createTime }} </template>
          </el-table-column>
        </el-table>
      </el-row>
    </div>
    <el-row display="margin-top:10px">
      <el-input id="query" v-model="input4" placeholder="请输入病人ID编号"
        style="display:inline-table; width: 12%; float:right"></el-input>
      <div id="step10" style="float:right;">
        <el-button type="primary" @click="delete_items()" style="float:right; margin: 2px;">删除指定项</el-button>
      </div>
    </el-row>
    <div id="step11">
      <el-row>
        <el-table :data="patientList" stripe style="width: 100%" border max-height="1000">
          <!--
    <el-table-column label="选项" type="selection" width="60" align="center">
      </el-table-column>
      -->
          <el-table-column sortable prop="patientId" label="病历ID" min-width="100">
            <template v-slot="scope"> {{ scope.row.pk }} </template>
          </el-table-column>
          <el-table-column prop="patientName" label="病人姓名" min-width="100">
            <template v-slot="scope"> {{ scope.row.fields.patientName }} </template>
          </el-table-column>
          <el-table-column prop="diseaseKind" label="病种" min-width="100">
            <template v-slot="scope"> {{ scope.row.fields.diseaseKind }} </template>
          </el-table-column>
          <el-table-column prop="videoUrl" label="视频url" min-width="100">
            <template v-slot="scope"> {{ scope.row.fields.videoUrl }} </template>
          </el-table-column>
          <el-table-column prop="faceUrlSelf" label="面象url" min-width="100">
            <template v-slot="scope"> {{ scope.row.fields.faceUrlSelf }} </template>
          </el-table-column>
          <el-table-column prop="tongueUrlSelf" label="舌象url" min-width="100">
            <template v-slot="scope"> {{ scope.row.fields.tongueUrlSelf }} </template>
          </el-table-column>
          <el-table-column prop="faceUrlStd" label="基准面象url" min-width="100">
            <template v-slot="scope"> {{ scope.row.fields.faceUrlStd }} </template>
          </el-table-column>
          <el-table-column prop="tongueUrlStd" label="基准舌象url" min-width="100">
            <template v-slot="scope"> {{ scope.row.fields.tongueUrlStd }} </template>
          </el-table-column>
          <el-table-column prop="createTime" label="添加时间" min-width="100">
            <template v-slot="scope"> {{ scope.row.fields.createTime }} </template>
          </el-table-column>
        </el-table>
      </el-row>
    </div>
    <v-tour name="myTour" :steps="steps" :options="myOptions"></v-tour>
  </div>
</template>

<script>

export default {
  name: 'home',
  data() {
    return {
      myOptions: {
        useKeyboardNavigation: false, // 是否通过键盘的←, → 和 ESC 控制指引
        labels: { // 指引项的按钮文案
          buttonSkip: "跳过指引", // 跳过文案
          buttonPrevious: "上一步", // 上一步文案
          buttonNext: "下一步", // 下一步文案
          buttonStop: "结束" // 结束文案
        },
        highlight: false // 是否高亮显示激活的的target项
      },
      steps: [
        {
          target: "#step1", // 当前项的id或class或data-v-step属性
          content: "点此打开摄像头预览，若长时间无反应请刷新网页重试", // 当前项指引内容
          params: {
            placement: "bottom", // 指引在target的位置，支持上、下、左、右
            highlight: false, // 当前项激活时是否高亮显示
            enableScrolling: false // 指引到当前项时是否滚动轴滚动到改项位置
          },
          before: type => new Promise((resolve, reject) => {
            resolve('foo')
          })
        },
        {
          target: "#step2", // 当前项的id或class或data-v-step属性
          content: "在此会显示实时摄像头预览界面", // 当前项指引内容
          params: {
            placement: "bottom", // 指引在target的位置，支持上、下、左、右
            highlight: false, // 当前项激活时是否高亮显示
            enableScrolling: false // 指引到当前项时是否滚动轴滚动到改项位置
          },
        },
        {
          target: "#step3", // 当前项的id或class或data-v-step属性
          content: "第一步，录入病人病历ID，录入病人姓名，会在第二张表单回显", // 当前项指引内容
          params: {
            placement: "bottom", // 指引在target的位置，支持上、下、左、右
            highlight: false, // 当前项激活时是否高亮显示
            enableScrolling: false // 指引到当前项时是否滚动轴滚动到改项位置
          },
        },
        {
          target: "#step4", // 当前项的id或class或data-v-step属性
          content: "开始录制按钮，跳出弹窗提示录制，点击弹窗中的结束录制停止录制", // 当前项指引内容
          params: {
            placement: "bottom", // 指引在target的位置，支持上、下、左、右
            highlight: false, // 当前项激活时是否高亮显示
            enableScrolling: false // 指引到当前项时是否滚动轴滚动到改项位置
          },
        },
        {
          target: "#step5", // 当前项的id或class或data-v-step属性
          content: "结束录制后在此输入病人ID，添加视频到数据库，若后台程序中断，一定要删掉该ID病人重新录制！或在程序media文件夹下检查视频是否存在，留待后续添加", // 当前项指引内容
          params: {
            placement: "bottom", // 指引在target的位置，支持上、下、左、右
            highlight: false, // 当前项激活时是否高亮显示
            enableScrolling: false // 指引到当前项时是否滚动轴滚动到改项位置
          },
        },
        {
          target: "#step6", // 当前项的id或class或data-v-step属性
          content: "在这里可以查询指定姓名的病人条目", // 当前项指引内容
          params: {
            placement: "bottom", // 指引在target的位置，支持上、下、左、右
            highlight: false, // 当前项激活时是否高亮显示
            enableScrolling: false // 指引到当前项时是否滚动轴滚动到改项位置
          },
        },
        {
          target: "#step7", // 当前项的id或class或data-v-step属性
          content: "对指定ID的病人添加病种大类", // 当前项指引内容
          params: {
            placement: "bottom", // 指引在target的位置，支持上、下、左、右
            highlight: false, // 当前项激活时是否高亮显示
            enableScrolling: false // 指引到当前项时是否滚动轴滚动到改项位置
          },
        },
        {
          target: "#step8", // 当前项的id或class或data-v-step属性
          content: "对于从手机同步到指定电脑文件夹的文件，可通过该功能上传到数据库", // 当前项指引内容
          params: {
            placement: "bottom", // 指引在target的位置，支持上、下、左、右
            highlight: false, // 当前项激活时是否高亮显示
            enableScrolling: false // 指引到当前项时是否滚动轴滚动到改项位置
          },
        },
        {
          target: "#step9", // 当前项的id或class或data-v-step属性
          content: "该表为查询指定姓名病人返回的数据表单", // 当前项指引内容
          params: {
            placement: "bottom", // 指引在target的位置，支持上、下、左、右
            highlight: false, // 当前项激活时是否高亮显示
            enableScrolling: false // 指引到当前项时是否滚动轴滚动到改项位置
          },
        },
        {
          target: "#step10", // 当前项的id或class或data-v-step属性
          content: "误添加后通过该功能删除指定ID的病人条目", // 当前项指引内容
          params: {
            placement: "bottom", // 指引在target的位置，支持上、下、左、右
            highlight: false, // 当前项激活时是否高亮显示
            enableScrolling: true // 指引到当前项时是否滚动轴滚动到改项位置
          },
        },
        {
          target: "#step11", // 当前项的id或class或data-v-step属性
          content: "该表单实时回显数据库中所有病人条目，ID为病人的唯一身份标识", // 当前项指引内容
          params: {
            placement: "bottom", // 指引在target的位置，支持上、下、左、右
            highlight: false, // 当前项激活时是否高亮显示
            enableScrolling: true // 指引到当前项时是否滚动轴滚动到改项位置
          },
        },
        {
          target: "#step12", // 当前项的id或class或data-v-step属性
          content: "结束工作后记得关闭摄像头，若重复关闭打开可能导致后台程序崩溃，请打开PyCharm重新输入指令运行", // 当前项指引内容
          params: {
            placement: "bottom", // 指引在target的位置，支持上、下、左、右
            highlight: false, // 当前项激活时是否高亮显示
            enableScrolling: true // 指引到当前项时是否滚动轴滚动到改项位置
          },
        },
      ],
      ImageUrl: '',
      input1: '',
      input2: '',
      input3: '',
      input4: '',
      input5: '',
      input6: '',
      input7: '',
      patientList: [],
      thePatient: [],
      selected_items: {},
      dialogVisible: false,
      dialogVisible1: false,
      intervalId: null,
    }
  },
  mounted: function () {
    this.show_patient()
    this.$tours["myTour"].start();
  },
  methods: {
    save_patient() {
      this.$http.get('http://127.0.0.1:8000/backend/save_patient', {
        params: {
          patient_id: this.input7,
          patient_name: this.input1  // 补全查询参数
        }
      })
        .then((response) => {
          const res = JSON.parse(response.bodyText);
          if (res.respCode === '000000') {
            this.show_patient()
          } else {
            this.$message.error('新增病人条目失败，ID可能重复，请重试')
            console.log(res['respMsg'])
          }
        })
    },
    disease_kind() {
      this.$http.get('http://127.0.0.1:8000/backend/disease_kind', {
        params: {
          patient_id: this.input5,
          patient_disease: this.input6  // 补全查询参数
        }
      })
        .then((response) => {
          const res = JSON.parse(response.bodyText);
          if (res.respCode === '000000') {
            this.show_patient()
          } else {
            this.$message.error('新增病人病种失败，请重试')
            console.log(res['respMsg'])
          }
        })
    },
    update_patient() {
      this.$http.get('http://127.0.0.1:8000/backend/update_patient?patient_id=' + this.input2)
        .then((response) => {
          const res = JSON.parse(response.bodyText);
          if (res.respCode === '000000') {
            this.show_patient()
          } else {
            this.$message.error('添加指定病人视频url失败，请重试或重新录制')
            console.log(res['respMsg'])
          }
        })
    },
    start_camera() {
      this.ImageUrl = ''
      setTimeout(() => {
        this.ImageUrl = 'http://127.0.0.1:8000/backend/start_camera';
      }, 100); // 停顿 0.1s，单位是毫秒
    },
    stop_camera() {
      this.$http.get('http://127.0.0.1:8000/backend/stop_camera')
    },
    start_record() {
      this.$http.get('http://127.0.0.1:8000/backend/start_record')
      this.dialogVisible1 = true
      //this.intervalId = setInterval(() => {
      //  this.timer++;
      //}, 1000);
    },
    stop_record() {
      this.$http.get('http://127.0.0.1:8000/backend/stop_record')
      this.dialogVisible1 = false
      //clearInterval(this.intervalId);
      //this.resetTimer();
    },
    show_patient() {
      this.$http.get('http://127.0.0.1:8000/backend/show_patient')
        .then((response) => {
          const res = JSON.parse(response.bodyText);
          console.log(res)
          if (res.respCode === '000000') {
            this.patientList = res['list']
          } else {
            this.$message.error('加载病人条目失败')
            console.log(res['respMsg'])
          }
        })
    },
    inquire_patient() {
      this.$http.get('http://127.0.0.1:8000/backend/inquire_patient?patient_name=' + this.input3)
        .then((response) => {
          const res = JSON.parse(response.bodyText);
          console.log(res)
          if (res.respCode === '000000') {
            this.thePatient = res['list']
          } else {
            this.$message.error('查询病人条目失败')
            console.log(res['respMsg'])
          }
        })
    },
    upload_images() {
      this.dialogVisible = true; // 显示弹窗
      this.$http.get('http://127.0.0.1:8000/backend/upload_images')
        .then((response) => {
          const res = JSON.parse(response.bodyText);
          console.log(res)
          if (res.respCode === '000000') {
            this.show_patient()
          } else {
            this.$message.error('上传图片失败')
            console.log(res['respMsg'])
          }
        })
      this.dialogVisible = false; // 隐藏弹窗
    },
    delete_items() {
      this.$http.get('http://127.0.0.1:8000/backend/delete_items?patient_id=' + this.input4)
        .then((response) => {
          const res = JSON.parse(response.bodyText);
          console.log(res)
          if (res.respCode === '000000') {
            this.show_patient()
          } else {
            this.$message.error('删除失败')
            console.log(res['respMsg'])
          }
        })
    },
    //resetTimer() {
    //  this.timer = 0; // 重置计时
    //},
    //handleSelectionChange(selection) {
    //  this.selected_items += selection;
    //},
  }
}

</script>

<style scoped>
h1,
h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}

.custom-dialog {
  width: 500px;
  /* 设置宽度 */
  height: 500px;
  /* 设置高度 */
}</style>
