<template>
  <div class="farm-page">
    <h2>农事管理中心</h2>
    <p class="subtitle">记录农事操作、跟踪作物生长阶段，并及时发现设备异常。</p>

    <div class="summary-grid">
      <div class="summary-card">
        <span class="summary-title">农田总数</span>
        <span class="summary-value">{{ summary.total_fields || 0 }}</span>
      </div>
      <div class="summary-card">
        <span class="summary-title">进行中任务</span>
        <span class="summary-value">{{ summary.active_tasks || 0 }}</span>
      </div>
      <div class="summary-card">
        <span class="summary-title">待执行任务</span>
        <span class="summary-value">{{ summary.pending_tasks || 0 }}</span>
      </div>
      <div class="summary-card">
        <span class="summary-title">设备异常</span>
        <span class="summary-value">{{ summary.fault_count || 0 }}</span>
      </div>
    </div>

    <section class="panel-card alert-panel">
      <div class="panel-title-row">
        <h3>农事建议报表</h3>
        <span class="alert-count">{{ report.pending_tasks || 0 }} 项待办</span>
      </div>
      <div class="report-grid">
        <div class="report-card">
          <span class="summary-title">待执行任务</span>
          <span class="summary-value">{{ report.pending_tasks || 0 }}</span>
        </div>
        <div class="report-card">
          <span class="summary-title">已完成任务</span>
          <span class="summary-value">{{ report.completed_tasks || 0 }}</span>
        </div>
        <div class="report-card">
          <span class="summary-title">设备故障</span>
          <span class="summary-value">{{ report.fault_count || 0 }}</span>
        </div>
        <div class="report-card">
          <span class="summary-title">天气预警</span>
          <span class="summary-value">{{ report.weather_warning_count || 0 }}</span>
        </div>
      </div>
      <div class="recommendations">
        <h4>操作建议</h4>
        <ul>
          <li v-for="item in report.recommendations || []" :key="item">{{ item }}</li>
        </ul>
      </div>
    </section>

    <section class="panel-card alert-panel">
      <div class="panel-title-row">
        <h3>联动提醒</h3>
        <span class="alert-count">{{ alerts.length }} 条</span>
      </div>
      <div v-if="alerts.length === 0" class="empty">目前暂无联动提醒。</div>
      <div v-else v-for="alert in alerts" :key="alert.id" class="alert-item">
        <div>
          <strong>{{ alert.title }}</strong>
          <p>{{ alert.message }}</p>
        </div>
        <span :class="['alert-badge', alert.type]">{{ alert.type === 'device_fault' ? '设备' : alert.type === 'weather_warning' ? '天气' : '任务' }}</span>
      </div>
    </section>

    <div class="panel-grid">
      <section class="panel-card">
        <div class="panel-title-row">
          <h3>农事记录与任务</h3>
          <button class="primary-btn" @click="openTaskModal()">新增任务</button>
        </div>

        <form class="task-form" @submit.prevent="submitTaskForm">
          <div class="form-row">
            <label>任务名称</label>
            <input v-model="taskForm.title" placeholder="如：晨间补水" required />
          </div>
          <div class="form-row">
            <label>农田</label>
            <input v-model="taskForm.field_name" placeholder="如：北区番茄田" required />
          </div>
          <div class="form-row">
            <label>任务类型</label>
            <input v-model="taskForm.task_type" placeholder="浇水 / 施肥 / 喷药 / 采收" required />
          </div>
          <div class="form-row">
            <label>描述</label>
            <textarea v-model="taskForm.description" rows="3" placeholder="描述任务内容"></textarea>
          </div>
          <div class="form-row">
            <label>计划时间</label>
            <input v-model="taskForm.scheduled_at" type="datetime-local" />
          </div>
          <div class="form-row">
            <label>状态</label>
            <select v-model="taskForm.status">
              <option value="待执行">待执行</option>
              <option value="进行中">进行中</option>
              <option value="已完成">已完成</option>
            </select>
          </div>
          <div class="form-actions">
            <button type="submit" class="primary-btn">{{ editingTaskId ? '保存修改' : '添加任务' }}</button>
            <button v-if="editingTaskId" type="button" class="secondary-btn" @click="cancelEdit">取消</button>
          </div>
        </form>

        <div v-for="task in sortedTasks" :key="task.id" class="task-item" :class="getTaskItemClass(task)">
          <div>
            <strong>{{ task.title }}</strong>
            <p>{{ task.field_name }} · {{ task.task_type }}</p>
            <p>{{ task.description }}</p>
            <p class="task-time">计划：{{ formatTaskTime(task.scheduled_at) }}</p>
          </div>
          <div class="task-actions">
            <span :class="['task-status', task.status]">{{ task.status }}</span>
            <button class="secondary-btn" @click="editTask(task)">编辑</button>
            <button v-if="task.status !== '已完成'" class="primary-btn" @click="completeTask(task.id)">完成</button>
            <button class="secondary-btn danger-btn" @click="deleteTask(task.id)">删除</button>
          </div>
        </div>
      </section>

      <section class="panel-card">
        <h3>作物生长周期</h3>
        <div v-for="stage in growthStages" :key="stage.crop_type + stage.stage" class="stage-item">
          <div class="stage-top">
            <strong>{{ stage.crop_type }} · {{ stage.stage }}</strong>
            <span>{{ stage.progress }}%</span>
          </div>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: stage.progress + '%' }"></div>
          </div>
          <p>{{ stage.description }}</p>
        </div>
      </section>
    </div>

    <section class="panel-card fault-panel">
      <h3>设备故障监测</h3>
      <div v-if="faults.length === 0" class="empty">当前暂无设备异常。</div>
      <div v-else v-for="fault in faults" :key="fault.id" class="fault-item">
        <div>
          <strong>{{ fault.device_name }}</strong>
          <p>{{ fault.fault }} · {{ fault.message }}</p>
        </div>
        <span class="fault-badge">异常</span>
      </div>
    </section>
  </div>
</template>

<script>
import { computed, defineComponent, ref, onMounted } from 'vue'
import api from '../../services/api'

export default defineComponent({
  name: 'FarmOperations',
  setup() {
    const tasks = ref([])
    const growthStages = ref([])
    const faults = ref([])
    const summary = ref({})
    const report = ref({ pending_tasks: 0, completed_tasks: 0, fault_count: 0, weather_warning_count: 0, recommendations: [] })
    const alerts = ref([])
    const editingTaskId = ref(null)
    const taskForm = ref({
      title: '',
      field_name: '',
      task_type: '',
      description: '',
      status: '待执行',
      scheduled_at: '',
    })

    const resetTaskForm = () => {
      editingTaskId.value = null
      taskForm.value = {
        title: '',
        field_name: '',
        task_type: '',
        description: '',
        status: '待执行',
        scheduled_at: '',
      }
    }

    const openTaskModal = () => {
      resetTaskForm()
    }

    const fetchFarmData = async () => {
      try {
        const [taskRes, stageRes, faultRes, summaryRes, reportRes, alertRes] = await Promise.all([
          api.get('/api/farm/tasks'),
          api.get('/api/farm/growth-stages'),
          api.get('/api/farm/faults'),
          api.get('/api/farm/summary'),
          api.get('/api/farm/report'),
          api.get('/api/farm/alerts'),
        ])
        tasks.value = taskRes.data
        growthStages.value = stageRes.data
        faults.value = faultRes.data
        summary.value = summaryRes.data
        report.value = reportRes.data
        alerts.value = alertRes.data
      } catch (err) {
        console.error('加载农事管理数据失败:', err)
      }
    }

    const submitTaskForm = async () => {
      try {
        if (editingTaskId.value) {
          await api.put(`/api/farm/tasks/${editingTaskId.value}`, taskForm.value)
        } else {
          await api.post('/api/farm/tasks', taskForm.value)
        }
        resetTaskForm()
        await fetchFarmData()
      } catch (err) {
        console.error('保存任务失败:', err)
      }
    }

    const editTask = (task) => {
      editingTaskId.value = task.id
      taskForm.value = { ...task }
    }

    const cancelEdit = () => {
      resetTaskForm()
    }

    const completeTask = async (taskId) => {
      try {
        await api.post(`/api/farm/tasks/${taskId}/complete`)
        await fetchFarmData()
      } catch (err) {
        console.error('完成任务失败:', err)
      }
    }

    const formatTaskTime = (value) => {
      if (!value) return '未设置'
      const date = new Date(value)
      if (Number.isNaN(date.getTime())) return value
      return date.toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
    }

    const getTaskItemClass = (task) => {
      if (!task.scheduled_at || task.status === '已完成') return ''
      const target = new Date(task.scheduled_at)
      const now = new Date()
      if (target < now) return 'task-overdue'
      const diffHours = (target - now) / (1000 * 60 * 60)
      if (diffHours <= 24) return 'task-upcoming'
      return ''
    }

    const deleteTask = async (taskId) => {
      try {
        await api.delete(`/api/farm/tasks/${taskId}`)
        await fetchFarmData()
      } catch (err) {
        console.error('删除任务失败:', err)
      }
    }

    onMounted(() => {
      fetchFarmData()
    })

    return {
      tasks,
      growthStages,
      faults,
      summary,
      report,
      alerts,
      editingTaskId,
      taskForm,
      openTaskModal,
      submitTaskForm,
      editTask,
      cancelEdit,
      completeTask,
      deleteTask,
      formatTaskTime,
      getTaskItemClass,
      sortedTasks: computed(() => [...tasks.value].sort((a, b) => {
        const timeA = a.scheduled_at ? new Date(a.scheduled_at).getTime() : Number.MAX_SAFE_INTEGER
        const timeB = b.scheduled_at ? new Date(b.scheduled_at).getTime() : Number.MAX_SAFE_INTEGER
        return timeA - timeB
      })),
    }
  },
})
</script>

<style scoped>
.farm-page { display: grid; gap: 20px; }
.subtitle { color: #64748b; margin-top: -8px; }
.summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; }
.summary-card { background: white; padding: 18px; border-radius: 16px; box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06); }
.summary-title { display: block; color: #64748b; font-size: 13px; margin-bottom: 8px; }
.summary-value { font-size: 28px; font-weight: 700; color: #0f172a; }
.panel-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; }
.panel-card { background: white; border-radius: 18px; padding: 20px; box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06); }
.panel-card h3 { margin-top: 0; margin-bottom: 16px; color: #1d4ed8; }
.panel-title-row { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 12px; }
.alert-panel { margin-bottom: 8px; }
.alert-count { color: #64748b; font-size: 13px; }
.report-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; margin-bottom: 12px; }
.report-card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 12px; }
.recommendations { border-top: 1px solid #e2e8f0; padding-top: 12px; }
.recommendations ul { margin: 8px 0 0 18px; color: #475569; }
.recommendations li { margin-bottom: 6px; }
.alert-item { display: flex; justify-content: space-between; gap: 12px; align-items: center; padding: 10px 0; border-bottom: 1px solid #f1f5f9; }
.alert-item:last-child { border-bottom: none; }
.alert-badge { padding: 6px 10px; border-radius: 999px; font-size: 12px; font-weight: 700; }
.alert-badge.device_fault { background: #fee2e2; color: #b91c1c; }
.alert-badge.weather_warning { background: #fff7ed; color: #c2410c; }
.alert-badge.task_reminder { background: #dbeafe; color: #1d4ed8; }
.primary-btn, .secondary-btn { border: none; border-radius: 999px; padding: 8px 12px; cursor: pointer; font-weight: 600; }
.primary-btn { background: #2563eb; color: white; }
.secondary-btn { background: #e2e8f0; color: #0f172a; }
.danger-btn { background: #fee2e2; color: #b91c1c; }
.task-form { display: grid; gap: 10px; margin-bottom: 14px; padding: 12px; border: 1px solid #e2e8f0; border-radius: 12px; background: #f8fafc; }
.form-row { display: grid; gap: 6px; }
.form-row label { font-size: 13px; color: #334155; font-weight: 600; }
.form-row input, .form-row textarea, .form-row select { width: 100%; border: 1px solid #cbd5e1; border-radius: 8px; padding: 8px 10px; font: inherit; }
.form-actions { display: flex; gap: 8px; }
.task-item, .fault-item { display: flex; justify-content: space-between; gap: 12px; align-items: center; padding: 12px 0; border-bottom: 1px solid #f1f5f9; }
.task-item.task-overdue { background: #fef2f2; border-radius: 10px; padding-left: 10px; padding-right: 10px; }
.task-item.task-upcoming { background: #fff7ed; border-radius: 10px; padding-left: 10px; padding-right: 10px; }
.task-actions { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
.task-time { color: #f59e0b; font-size: 12px; font-weight: 600; }
.task-item:last-child, .fault-item:last-child { border-bottom: none; }
.task-status { padding: 6px 10px; border-radius: 999px; font-size: 12px; font-weight: 700; }
.task-status.已完成 { background: #dcfce7; color: #166534; }
.task-status.进行中 { background: #dbeafe; color: #1d4ed8; }
.task-status.待执行 { background: #fef3c7; color: #92400e; }
.stage-item { margin-bottom: 14px; }
.stage-top { display: flex; justify-content: space-between; margin-bottom: 8px; }
.progress-bar { height: 8px; border-radius: 999px; background: #e2e8f0; overflow: hidden; margin-bottom: 6px; }
.progress-fill { height: 100%; background: linear-gradient(90deg, #10b981, #34d399); border-radius: inherit; }
.stage-item p, .task-item p, .fault-item p { margin: 4px 0 0; color: #64748b; font-size: 13px; }
.fault-badge { padding: 6px 10px; background: #fee2e2; color: #b91c1c; border-radius: 999px; font-size: 12px; font-weight: 700; }
.empty { color: #64748b; }
</style>
