from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Course, Teacher, CourseTeacher, Review
from flask_login import login_required, current_user
from forms import ReviewForm
from sqlalchemy.orm import joinedload
from sqlalchemy import func

course = Blueprint('course', __name__)



@course.route('/courses', methods=['GET'])
def list_courses():
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)  # 默认每页显示10条

    # 构建查询，明确使用 Course 作为 select_from 的起点
    courses_query = db.session.query(
        Course,
        func.count(Review.id).label('review_count')  # 计算每个课程的评论数量
    ).select_from(Course).outerjoin(
        CourseTeacher, CourseTeacher.course_id == Course.id  # 明确连接 CourseTeacher 的条件
    ).outerjoin(
        Review, Review.course_teacher_id == CourseTeacher.id  # 明确连接 Review 的条件
    ).options(
        joinedload(Course.course_teachers).joinedload(CourseTeacher.teacher)
    ).group_by(Course.id)  # 确保 group_by 的对象是明确的

    # 根据搜索条件过滤
    if search_query:
        courses_query = courses_query.filter(
            Course.course_name.ilike(f'%{search_query}%') |
            Course.course_code.ilike(f'%{search_query}%')
        )

    # 按评论数量降序排序，使有评论的课程优先
    courses_query = courses_query.order_by(func.count(Review.id).desc())

    # 对查询结果进行分页
    courses = courses_query.paginate(page=page, per_page=per_page)

    # 预处理教师和学期信息
    processed_courses = []
    for course, review_count in courses.items:
        teachers = {ct.teacher.name for ct in course.course_teachers}
        # 从 JSON 字段中提取学期信息
        semesters = {ct.semester_info['semester'] for ct in course.course_teachers if ct.semester_info}
        processed_courses.append({
            'course': course,
            'teachers': ', '.join(teachers),
            'semesters': ', '.join(semesters),
            'review_count': review_count  # 添加评论数量信息
        })

    return render_template(
        'course_list.html',
        courses=processed_courses,
        pagination=courses,
        search_query=search_query,
        per_page=per_page
    )



@course.route('/courses/<int:course_id>', methods=['GET'])
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    
    # 获取与该课程相关的教师和学期信息
    course_teachers = CourseTeacher.query.filter_by(course_id=course_id).all()

    # 处理教师和学期信息
    teachers_info = []
    for ct in course_teachers:
        # 从 JSONB 字段 semester_info 中提取学期名称
        semester_info = ct.semester_info or {}  # 确保如果字段为空不会抛出异常
        semester_name = semester_info.get('semester', '未指定学期')  # 假设学期名称存储在 'semester_name' 键下

        # 计算平均评分
        reviews_query = db.session.query(
            func.avg(Review.rating).label('average_rating')
        ).filter_by(course_teacher_id=ct.id).first()

        if reviews_query and reviews_query.average_rating is not None:
            average_rating = round(reviews_query.average_rating, 2)
        else:
            average_rating = '暂无评分'

        review_count = Review.query.filter_by(course_teacher_id=ct.id).count()
        
        teachers_info.append({
            'teacher_id': ct.teacher.id, 
            'teacher_name': ct.teacher.name,
            'teacher_title': ct.teacher.title,
            'semester_name': semester_name,
            'average_rating': average_rating,
            'review_count': review_count
        })

    return render_template('course_detail.html', course=course, teachers_info=teachers_info)




