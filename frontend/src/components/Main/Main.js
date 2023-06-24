import React, {useEffect, useState} from 'react';
import '../../App.css'

const InputForm = () => {
  const [isFormsFilled, setIsFormsFilled] = useState(false);

  const [obj_prg, setObjPrg] = useState('');
  const [obj_subprg, setObjSubprg] = useState('');
  const [obj_key, setObjKey] = useState('');
  const [task_code, setTaskCode] = useState('');
  const [task_name, setTaskName] = useState('');
  const [task_completion, setTaskCompletion] = useState('');
  const [task_start_date, setTaskStartDate] = useState('');
  const [task_end_date, setTaskEndDate] = useState('');
  const [bp_start_date, setBPStartDate] = useState('');
  const [bp_end_date, setBPEndDate] = useState('');
  const [status_expertise, setStatusExpertise] = useState('');
  const [expertise, setExpertise] = useState('');
  const [date_report, setDateReport] = useState('');

  const allFields = [
    obj_prg,
    obj_subprg,
    obj_key,
    task_code,
    task_name,
    task_completion,
    task_start_date,
    task_end_date,
    bp_start_date,
    bp_end_date,
    status_expertise,
    expertise,
    date_report
  ]

  const validateForms = () => {
    if (obj_prg && obj_subprg && obj_key && task_code && task_name && task_completion && task_start_date && task_end_date && bp_start_date && bp_end_date && status_expertise && expertise && date_report) {
      setIsFormsFilled(true);
    } else {
      setIsFormsFilled(false);
    }
  }

  useEffect(() => {
    validateForms();
  }, allFields)

  return (
    <div>
      <form className='forms'>
        <div>
          <p>obj_prg</p>
          <input type="text" value={obj_prg} onChange={(e) => setObjPrg(e.target.value)}/> <br/>
          <p>obj_subprg</p>
          <input type="text" value={obj_subprg} onChange={(e) => setObjSubprg(e.target.value)}/> <br/>
          <p>obj_key</p>
          <input type="text" value={obj_key} onChange={(e) => setObjKey(e.target.value)}/> <br/>
          <p>task_code</p>
          <input type="text" value={task_code} onChange={(e) => setTaskCode(e.target.value)}/> <br/>
        </div>
        <div>
          <p>task_name</p>
          <input type="text" value={task_name} onChange={(e) => setTaskName(e.target.value)}/> <br/>
          <p>task_completion</p>
          <input type="text" value={task_completion} onChange={(e) => setTaskCompletion(e.target.value)}/> <br/>
          <p>task_start_date</p>
          <input type="text" value={task_start_date} onChange={(e) => setTaskStartDate(e.target.value)}/> <br/>
          <p>task_end_date</p>
          <input type="text" value={task_end_date} onChange={(e) => setTaskEndDate(e.target.value)}/> <br/>
          <p>bp_start_date</p>
          <input type="text" value={bp_start_date} onChange={(e) => setBPStartDate(e.target.value)}/> <br/>
        </div>
        <div>
          <p>bp_end_date</p>
          <input type="text" value={bp_end_date} onChange={(e) => setBPEndDate(e.target.value)}/> <br/>
          <p>status_expertise</p>
          <input type="text" value={status_expertise} onChange={(e) => setStatusExpertise(e.target.value)}/> <br/>
          <p>expertise</p>
          <input type="text" value={expertise} onChange={(e) => setExpertise(e.target.value)}/> <br/>
          <p>date_report</p>
          <input type="text" value={date_report} onChange={(e) => setDateReport(e.target.value)}/>
        </div>
      </form>
        <button className={`${!isFormsFilled && "button__disabled"}`}>Рассчитать срок</button>

    </div>
  );
};

export default InputForm;